"""Tests for Movies Resource"""

import falcon


def test_heartbeat_get(client):
    result = client.simulate_get('/movies')
    assert result.status == falcon.HTTP_OK
