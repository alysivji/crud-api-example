"""Tests for Movies Resource"""

import falcon


def test_movies_get(client):
    result = client.simulate_get('/movies')
    assert result.status == falcon.HTTP_OK


def test_movies_post_get_put_delete(client):
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
