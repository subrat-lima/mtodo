import pytest


class TestBaseBlueprint:
    def test_index(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "<title>mtodo</title>" in response.text

    def test_error_handler(self, client):
        response = client.get("/invalid")
        assert response.status_code == 404
        assert "404 Not Found" in response.text

    def test_logout(self, client):
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert len(response.history) == 1
        assert "you have logged out" in response.text
