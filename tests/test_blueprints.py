import json

import pytest

from mtodo.models import OAuth, Todo, User, db


class TestBaseBlueprint:
    def test_index(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "<title>mtodo</title>" in response.text

    def test_error_handler(self, client):
        response = client.get("/invalid")
        assert response.status_code == 404
        assert "404 Not Found" in response.text

    def test_logout(self, client):
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert len(response.history) == 1
        assert "you have logged out" in response.text


class TestTodoBlueprint:
    def test_add(self, default_loggedin_user):
        response = default_loggedin_user.post(
            "/api/todos",
            data=json.dumps({"text": "task 1", "done": False}),
            headers={"content-type": "application/json"},
            follow_redirects=True,
        )
        todo = db.session.query(Todo).first()
        assert response.status_code == 200
        assert response.json["status"] == True
        assert response.json["text"] == "todo added"
        assert response.json["id"] == todo.id

    def test_get(self, default_todo):
        response = default_todo.get("/api/todos", follow_redirects=True)
        todo = db.session.query(Todo).first()
        assert response.status_code == 200
        assert response.json["status"] == True
        assert response.json["data"] is not None
        assert len(response.json["data"]) == 1
        assert response.json["data"][0]["user_id"] == todo.user.id
        assert response.json["data"][0]["text"] == "task 1"
        assert response.json["data"][0]["done"] == False

    def test_update(self, default_todo):
        todo = db.session.query(Todo).first()
        response = default_todo.put(
            f"/api/todos/{todo.id}",
            data=json.dumps({"done": True}),
            headers={"content-type": "application/json"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.json["status"] == True
        assert response.json["text"] == "todo updated"

        response = default_todo.get("/api/todos", follow_redirects=True)
        todo = db.session.query(Todo).first()
        assert response.status_code == 200
        assert response.json["status"] == True
        assert response.json["data"] is not None
        assert len(response.json["data"]) == 1
        assert response.json["data"][0]["user_id"] == todo.user.id
        assert response.json["data"][0]["text"] == "task 1"
        assert response.json["data"][0]["done"] == True

    def test_delete(self, default_todo):
        todo = db.session.query(Todo).first()
        response = default_todo.delete(f"/api/todos/{todo.id}", follow_redirects=True)
        assert response.status_code == 200
        assert response.json["status"] == True
        assert response.json["text"] == "todo deleted"

        response = default_todo.get("/api/todos", follow_redirects=True)
        assert response.status_code == 200
        assert response.json["status"] == True
        assert response.json["data"] is not None
        assert len(response.json["data"]) == 0
