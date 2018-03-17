"""Tests for Movies Resource"""

import falcon
import pytest


@pytest.fixture
def populate_db(client):
    """
    Fixture to populate database and delete after running tests

    Insert each element one at a time
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

        for i in range(num_entries_to_insert):
            result = client.simulate_post('/movies', json=movie_to_enter)
            created_id = result.headers['location'].split('/')[-1]
            inserted_ids.append(created_id)

    yield _insert_item

    for id_ in inserted_ids:
        client.simulate_delete(f'/movies/{id_}')


def test_movies_get_list(client, populate_db):
    # Arrange
    NUM_RECORDS = 5
    populate_db(num_entries_to_insert=NUM_RECORDS)

    # Act
    result = client.simulate_get('/movies')

    # Assert
    assert result.status == falcon.HTTP_OK
    assert len(result.json) == NUM_RECORDS


def test_movies_get_list_no_records(client):
    """
    Test getting list of movies from empty database
    """

    result = client.simulate_get('/movies')
    assert result.status == falcon.HTTP_NOT_FOUND


def test_movies_get_single_item_not_found(client):
    """
    Test getting a single movie that does is not in database
    """
    result = client.simulate_get('/movies/927402')
    assert result.status == falcon.HTTP_NOT_FOUND


def test_movies_post_get_put_delete(client):
    """
    Test inserting movie, getting it, changing attribute, and deleting it
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
