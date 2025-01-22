from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from mtodo.models import OAuth, User, db


@pytest.fixture
def default_user(app):
    user = User(email="john@email.com")
    db.session.add(user)
    db.session.commit()


@pytest.fixture
def default_oauth(default_user):
    user = db.session.query(User).first()
    oauth = OAuth(
        provider="dummy-provider",
        provider_user_id="5",
        user_id=user.id,
        token={"key": "value"},
    )
    db.session.add(oauth)
    db.session.commit()


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
