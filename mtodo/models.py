import uuid
from dataclasses import dataclass

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_uuid():
    return uuid.uuid4().hex


class User(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True, default=get_uuid)
    email = db.Column(db.String(256), unique=True, nullable=False)
    todos = db.relationship("Todo", backref="user")


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


@dataclass
class Todo(db.Model):
    id: str
    user_id: int
    text: str
    done: bool

    id = db.Column(db.String, primary_key=True, default=get_uuid)
    text = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    __table_args__ = (db.UniqueConstraint("text", "user_id", name="user_todo"),)


login_manager = LoginManager()
login_manager.login_view = "google.login"


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, id)
