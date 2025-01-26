import json

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_socketio import emit, send
from werkzeug.exceptions import HTTPException

from ..extensions import socketio
from ..models import Todo, db

bp = Blueprint("todos", __name__, url_prefix="/api/todos")


@bp.route("/")
@login_required
def get():
    todos = db.session.query(Todo).filter_by(user_id=current_user.id).all()
    response = {"status": True, "data": todos}
    return jsonify(response)


@bp.route("/", methods=["POST"])
@login_required
def add():
    room = str(current_user.id)
    data = request.json
    if data["text"] == "":
        return jsonify({"status": False, "text": "text empty"})
    query = (
        db.session.query(Todo)
        .filter_by(user_id=current_user.id, text=data["text"])
        .first()
    )
    if query is not None:
        return jsonify({"status": False, "text": "todo exists"})
    todo = Todo(text=data["text"], done=data["done"], user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    socketio.emit(
        "add-todo",
        json.dumps({"id": todo.id, "text": todo.text, "done": todo.done}),
        to=room,
    )
    return jsonify({"status": True, "text": "todo added", "id": todo.id})


@bp.route("/<id>", methods=["PUT"])
@login_required
def update(id):
    todo = db.session.get(Todo, id)
    if current_user.id != todo.user_id:
        return jsonify({"status": False, "text": "unauthorized access"})
    room = str(current_user.id)
    data = request.json

    todo.done = data["done"]
    db.session.add(todo)
    db.session.commit()
    socketio.emit(
        "update-todo", json.dumps({"id": todo.id, "done": todo.done}), to=room
    )
    return jsonify({"status": True, "text": "todo updated"})


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(id):
    todo = db.session.get(Todo, id)
    if current_user.id != todo.user_id:
        return jsonify({"status": False, "text": "unauthorized access"})
    room = str(current_user.id)
    db.session.delete(todo)
    db.session.commit()
    socketio.emit("delete-todo", json.dumps({"id": todo.id}), to=room)
    return jsonify({"status": True, "text": "todo deleted"})
