from flask import flash
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.google import google, make_google_blueprint
from flask_login import current_user, login_user

from ..models import OAuth, User, db

bp = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)


@oauth_authorized.connect_via(bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("failed to log in.", category="error")
        return False

    resp = google.get("/oauth2/v1/userinfo")
    if not resp.ok:
        flash("failed to fetch user info.", category="error")
        return False

    info = resp.json()
    user_id = info["id"]

    oauth = (
        db.session.query(OAuth)
        .filter_by(provider=blueprint.name, provider_user_id=user_id)
        .first()
    )
    if oauth is None:
        user = User(email=info["email"])
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
    login_user(oauth.user)
    flash("sucessfully signed in.", category="info")
    return False


@oauth_error.connect_via(bp)
def google_error(blueprint, message, response):
    msg = f"oauth error from {blueprint.name}! message={message} response={response}"
    flash(msg, category="error")
