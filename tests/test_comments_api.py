from fastapi.testclient import TestClient
from app.main import app
from app import storage
from app.comments import _reset_comments

client = TestClient(app)


def setup_function():
    storage._reset()
    _reset_comments()


def test_comments_create_list_delete_flow():
    # create a task
    r = client.post("/tasks", json={"title": "task for comments"})
    assert r.status_code == 201
    task = r.json()
    tid = task["id"]

    # add a comment (valid)
    r2 = client.post(f"/tasks/{tid}/comments", json={"text": "First"})
    assert r2.status_code == 201
    c = r2.json()
    assert "id" in c and c["text"] == "First"

    # list comments
    r3 = client.get(f"/tasks/{tid}/comments")
    assert r3.status_code == 200
    arr = r3.json()
    assert isinstance(arr, list) and len(arr) == 1

    # delete comment
    r4 = client.delete(f"/tasks/{tid}/comments/{c['id']}")
    assert r4.status_code == 204

    # now list is empty
    r5 = client.get(f"/tasks/{tid}/comments")
    assert r5.status_code == 200
    assert r5.json() == []


def test_create_blank_comment_returns_422():
    r = client.post("/tasks", json={"title": "t"})
    assert r.status_code == 201
    tid = r.json()["id"]

    r2 = client.post(f"/tasks/{tid}/comments", json={"text": "   "})
    assert r2.status_code == 422


def test_comment_on_missing_task_returns_404():
    fake = "doesnotexist"
    r = client.post(f"/tasks/{fake}/comments", json={"text": "hi"})
    assert r.status_code == 404


def test_delete_missing_comment_returns_404():
    r = client.post("/tasks", json={"title": "t2"})
    assert r.status_code == 201
    tid = r.json()["id"]

    r2 = client.delete(f"/tasks/{tid}/comments/notfound")
    assert r2.status_code == 404
