import pytest
from flask_login import FlaskLoginClient, login_user

from mtodo import create_app
from mtodo.models import OAuth, Todo, User, db


@pytest.fixture
def app():
    test_config = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    app = create_app(test_config)
    app.test_client_class = FlaskLoginClient
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def default_user(client):
    user = User(email="john@email.com")
    db.session.add(user)
    db.session.commit()
    return client


@pytest.fixture
def default_oauth(default_user):
    user = db.session.query(User).first()
    oauth = OAuth(
        provider="dummy-provider",
        provider_user_id="5",
        user_id=user.id,
        token={"key": "value"},
    )
    db.session.add_all([user, oauth])
    db.session.commit()
    return default_user


@pytest.fixture
def default_loggedin_user(app):
    user = User(email="john@email.com")
    db.session.add(user)
    db.session.commit()
    return app.test_client(user=user)


@pytest.fixture
def default_todo(default_loggedin_user):
    user = db.session.query(User).first()
    todo = Todo(text="task 1", done=False, user_id=user.id)
    db.session.add(todo)
    db.session.commit()
    return default_loggedin_user
