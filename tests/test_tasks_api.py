from fastapi.testclient import TestClient
from app.main import app
from app import storage
from app.comments import _reset_comments

client = TestClient(app)


def setup_function():
    storage._reset()
    _reset_comments()


def test_create_and_search_and_filter():
    r1 = client.post(
        "/tasks",
        json={"title": "Auth work", "description": "auth", "status": "ToDo", "priority": "High", "assignee": "maya"},
    )
    assert r1.status_code == 201

    r2 = client.post(
        "/tasks",
        json={"title": "UI polish", "description": "style", "status": "InProgress", "priority": "Medium", "assignee": "alex"},
    )
    assert r2.status_code == 201

    # search by text
    r = client.get("/tasks?q=auth")
    assert r.status_code == 200
    data = r.json()
    assert any("Auth work" == t["title"] for t in data) or any(
        "auth" in (t.get("description") or "").lower() for t in data
    )

    # combined filters
    r = client.get("/tasks?status=InProgress&priority=Medium&assignee=alex")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["title"] == "UI polish"


def test_invalid_enum_returns_422():
    r = client.get("/tasks?status=BadValue")
    assert r.status_code == 422
