from mtodo import create_app


def test_base_config():
    assert not create_app().testing


def test_invalid_path(client):
    response = client.get("/invalid")
    assert response.status_code == 404


def test_valid_path(client):
    response = client.get("/")
    assert response.status_code == 200
