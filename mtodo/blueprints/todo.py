from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.exceptions import HTTPException

from ..models import Todo, db

bp = Blueprint("todos", __name__, url_prefix="/api/todos")


@bp.route("/")
@login_required
def get():
    todos = db.session.query(Todo).all()
    response = {"status": True, "data": todos}
    return jsonify(response)


@bp.route("/", methods=["POST"])
@login_required
def add():
    data = request.json
    todo = Todo(text=data["text"], done=data["done"], user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    return jsonify({"status": True, "text": "todo added", "id": todo.id})


@bp.route("/<int:id>", methods=["PUT"])
@login_required
def update(id):
    data = request.json
    todo = db.session.get(Todo, id)
    todo.done = data["done"]
    db.session.add(todo)
    db.session.commit()
    return jsonify({"status": True, "text": "todo updated"})


@bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete(id):
    todo = db.session.get(Todo, id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"status": True, "text": "todo deleted"})
