import os

from flask import Flask, render_template
from werkzeug.exceptions import HTTPException


def create_app(config_obj={}):
    app = Flask(__name__)

    app.config.update(config_obj)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(HTTPException)
    def handle_error(error):
        message = f"{error.code} {error.name}"
        return render_template("error.html", message=message), error.code

    return app
