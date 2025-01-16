import pytest

from mtodo import create_app


@pytest.fixture
def app():
    test_config = {"TESTING": True}
    app = create_app(test_config)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
