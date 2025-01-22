from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import logout_user
from werkzeug.exceptions import HTTPException

bp = Blueprint("base", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.app_errorhandler(HTTPException)
def handle_error(error):
    message = f"{error.code} {error.name}"
    return render_template("error.html", error_message=message), error.code


@bp.route("/logout")
def logout():
    logout_user()
    flash("you have logged out", "info")
    return redirect(url_for("base.index"))
