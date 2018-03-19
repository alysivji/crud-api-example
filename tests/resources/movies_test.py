"""Tests for Movies Resource"""

import falcon
import pytest

from app.config import PAGE_SIZE


@pytest.fixture
def populate_db(client):
    """
    Fixture to populate database and delete after running tests

    BULK insert items
    """
    movie_to_enter = {
        "title": "Return of the Jedi",
        "year": 1985,
        "description": "Ewoks gallore"
    }
    inserted_ids = []

    def _insert_item(num_entries_to_insert=1):
        """
        Insert item into database X number of times
        """
        movies = dict()
        movies['data'] = [movie_to_enter for _ in range(num_entries_to_insert)]

        result = client.simulate_post('/movies/bulk', json=movies)
        assert result.status == falcon.HTTP_CREATED
        last_created_id = int(result.headers['location'].split('/')[-1])

        # get list of ids created via bulk insert
        inserted_ids.extend(list(
            range(num_entries_to_insert + 1, last_created_id + 1)))

    yield _insert_item

    for id_ in inserted_ids:
        client.simulate_delete(f'/movies/{id_}')


def test_movies_get_list(client, populate_db):
    """
    Test GET list of movies
    """
    # Arrange
    NUM_RECORDS = 5
    populate_db(num_entries_to_insert=NUM_RECORDS)

    # Act
    result = client.simulate_get('/movies')

    # Assert
    assert result.status == falcon.HTTP_OK
    assert len(result.json['data']) == NUM_RECORDS
    assert result.json['last_id'] == result.json['data'][-1]['id']


def test_movies_get_list_nonint_param(client, populate_db):
    """
    Test GET list of movies with wrong type of query parameter
    """
    # Arrange
    NUM_RECORDS = 5
    populate_db(num_entries_to_insert=NUM_RECORDS)
    params = {'last_id': 'word'}

    # Act
    result = client.simulate_get('/movies', params=params)

    # Assert
    assert result.status == falcon.HTTP_UNPROCESSABLE_ENTITY


@pytest.mark.slow
def test_movies_get_list_paginated_less_than_one_page(client, populate_db):
    """
    Test GET list of movies with pagination
    """
    # Arrange
    NUM_RECORDS = PAGE_SIZE - 1
    populate_db(num_entries_to_insert=NUM_RECORDS)

    # Act
    result = client.simulate_get('/movies')

    # Assert
    assert result.status == falcon.HTTP_OK
    assert len(result.json['data']) == NUM_RECORDS
    assert result.json['last_id'] == result.json['data'][-1]['id']


@pytest.mark.slow
def test_movies_get_list_paginated_exactly_one_page(client, populate_db):
    """
    Test GET list of movies with pagination
    """
    # Arrange
    NUM_RECORDS = PAGE_SIZE
    populate_db(num_entries_to_insert=NUM_RECORDS)

    # Act
    result = client.simulate_get('/movies')

    # Assert
    assert result.status == falcon.HTTP_OK
    assert len(result.json['data']) == NUM_RECORDS
    last_id = result.json['data'][-1]['id']
    assert result.json['last_id'] == last_id

    """
    GET 2nd page (should not have any results)
    """
    params = {'last_id': last_id}

    # Act
    result = client.simulate_get('/movies', params=params)

    # Assert
    assert result.status == falcon.HTTP_NOT_FOUND


@pytest.mark.slow
def test_movies_get_list_paginated_greater_than_one_page(client, populate_db):
    """
    Test GET list of movies with pagination
    """
    # Arrange
    NUM_RECORDS = PAGE_SIZE + 1
    populate_db(num_entries_to_insert=NUM_RECORDS)

    # Act
    result = client.simulate_get('/movies')

    # Assert
    assert result.status == falcon.HTTP_OK
    assert len(result.json['data']) == PAGE_SIZE
    last_id = result.json['data'][-1]['id']
    assert result.json['last_id'] == last_id

    """
    GET 2nd page (should not have 1 entry)
    """
    params = {'last_id': last_id}

    # Act
    result = client.simulate_get('/movies', params=params)

    # Assert
    assert result.status == falcon.HTTP_OK
    assert len(result.json['data']) == 1
    assert result.json['last_id'] == result.json['data'][-1]['id']


def test_movies_get_list_empty_db(client):
    """
    Test GET list of movies from empty database
    """
    result = client.simulate_get('/movies')
    assert result.status == falcon.HTTP_NOT_FOUND


def test_movies_get_single_item_not_found(client):
    """
    Test GET a single movie that does is not in database
    """
    result = client.simulate_get('/movies/927402')
    assert result.status == falcon.HTTP_NOT_FOUND


def test_movies_put_not_found(client):
    """
    Test PUT a single movie that does is not in database
    """
    movie_to_update = {
        "title": "Return of the Jedi",
        "year": 1985,
        "description": "Ewoks gallore"
    }

    result = client.simulate_put('/movies/927402', json=movie_to_update)
    assert result.status == falcon.HTTP_NOT_FOUND


def test_movies_delete_not_found(client):
    """
    Test DELETE a single movie that does is not in database
    """
    result = client.simulate_delete('/movies/927402')
    assert result.status == falcon.HTTP_NOT_FOUND


def test_movies_lifecycle(client):
    """
    Test:
        * POST single movie
        * GET single movie
        * PUT attribute of single movie
        * DELETE single movie
    """

    movie_to_enter = {
        "title": "Return of the Jedi",
        "year": 1985,
        "description": "Ewoks gallore"
    }

    # POST
    result = client.simulate_post('/movies', json=movie_to_enter)

    assert result.status == falcon.HTTP_CREATED
    assert 'location' in result.headers

    created_id = result.headers['location'].split('/')[-1]

    # GET
    result = client.simulate_get(f'/movies/{created_id}')
    payload = result.json
    payload.pop('id')

    assert result.status == falcon.HTTP_OK
    assert payload == movie_to_enter

    # PUT
    movie_to_enter['year'] = 1983

    result = client.simulate_put(f'/movies/{created_id}', json=movie_to_enter)

    assert result.status == falcon.HTTP_OK

    # GET
    result = client.simulate_get(f'/movies/{created_id}')
    payload = result.json
    payload.pop('id')

    assert result.status == falcon.HTTP_OK
    assert payload == movie_to_enter

    # DELETE
    result = client.simulate_delete(f'/movies/{created_id}')

    assert result.status == falcon.HTTP_OK
