from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from mtodo.models import OAuth, Todo, User, db


class TestUser:
    def test_user_add(self, default_user):
        user = db.session.query(User).first()
        assert user is not None
        assert user.id is not None
        assert user.email == "john@email.com"

    @pytest.mark.parametrize("email", ["john@email.com", None])
    def test_user_constraints(self, default_user, email):
        with pytest.raises(IntegrityError):
            user = User(email=email)
            db.session.add(user)
            db.session.commit()


class TestOAuth:
    def test_oauth_add(self, default_oauth):
        user = db.session.query(User).first()
        oauth = db.session.query(OAuth).first()
        assert oauth is not None
        assert oauth.id is not None
        assert oauth.user == user
        assert oauth.provider_user_id == "5"
        assert oauth.token.get("key") == "value"

    @pytest.mark.parametrize(
        ("provider_user_id", "user_id"),
        [
            ("5", 2),
            (None, 1),
            ("6", None),
        ],
    )
    def test_oauth_constraints(self, default_oauth, provider_user_id, user_id):
        with pytest.raises(IntegrityError):
            oauth = OAuth(
                provider="dummy-provider",
                provider_user_id=provider_user_id,
                user_id=user_id,
                token={"key": "value"},
            )
            db.session.add(oauth)
            db.session.commit()


class TestTodo:
    def test_todo_add(self, default_todo):
        user = db.session.query(User).first()
        todo = db.session.query(Todo).first()
        assert todo is not None
        assert todo.id is not None
        assert todo.user == user
        assert todo.text == "task 1"
        assert todo.done == False

    @pytest.mark.parametrize(
        ("user_id", "text", "done"),
        [
            (1, "task 1", True),
            (None, "text", False),
            (1, None, False),
        ],
    )
    def test_todo_constraints(self, default_todo, user_id, text, done):
        with pytest.raises(IntegrityError):
            todo = Todo(text=text, done=done, user_id=user_id)
            db.session.add(todo)
            db.session.commit()
