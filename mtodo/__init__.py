import os

from dotenv import load_dotenv
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

from .blueprints import base, google, todo
from .models import db, login_manager

load_dotenv()


def create_app(config_obj={}):
    app = Flask(__name__)

    app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get(
        "MTODO_GOOGLE_OAUTH_CLIENT_ID"
    )
    app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get(
        "MTODO_GOOGLE_OAUTH_CLIENT_SECRET"
    )
    app.config["SECRET_KEY"] = os.environ.get("MTODO_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mtodo.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config.update(config_obj)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()

    app.register_blueprint(base.bp)
    app.register_blueprint(google.bp)
    app.register_blueprint(todo.bp)

    return app
