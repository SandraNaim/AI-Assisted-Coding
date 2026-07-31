import uuid

from fastapi.testclient import TestClient

from app.models import TaskStatus


def test_create_task_valid_returns_201_with_full_body(client: TestClient):
    payload = {
        "title": "Full task",
        "description": "A detailed task",
        "status": "ToDo",
        "priority": "High",
        "assignee": "alice",
    }
    r = client.post("/tasks", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Full task"
    assert body["description"] == "A detailed task"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "alice"
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_create_task_missing_title_returns_422(client: TestClient):
    r = client.post("/tasks", json={})
    assert r.status_code == 422


def test_create_task_blank_title_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "   "})
    assert r.status_code == 422


def test_create_task_invalid_priority_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "x", "priority": "Ultra"})
    assert r.status_code == 422


def test_create_task_unknown_field_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "x", "unknown": "y"})
    assert r.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client: TestClient):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client: TestClient, created_task):
    # created_task uses default status ToDo; filter by Done -> no match
    r = client.get("/tasks", params={"status": "Done"})
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client: TestClient):
    # Create two tasks with different priorities
    r1 = client.post("/tasks", json={"title": "low task", "priority": "Low"})
    assert r1.status_code == 201
    r2 = client.post("/tasks", json={"title": "high task", "priority": "High"})
    assert r2.status_code == 201

    r = client.get("/tasks", params={"priority": "High"})
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["priority"] == "High"


def test_get_task_by_id_returns_task(client: TestClient, created_task):
    task_id = created_task["id"]
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == task_id
    assert body["title"] == created_task["title"]


def test_get_task_by_id_not_found_returns_404_with_detail(client: TestClient):
    fake_id = uuid.uuid4().hex
    r = client.get(f"/tasks/{fake_id}")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == f"Task with id {fake_id} not found"


def test_patch_partial_update_keeps_other_fields(client: TestClient, created_task):
    task_id = created_task["id"]
    original_title = created_task["title"]
    r = client.patch(f"/tasks/{task_id}", json={"description": "updated description"})
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == task_id
    assert body["title"] == original_title  # unchanged
    assert body["description"] == "updated description"


def test_patch_not_found_returns_404(client: TestClient):
    fake_id = uuid.uuid4().hex
    r = client.patch(f"/tasks/{fake_id}", json={"description": "x"})
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == f"Task with id {fake_id} not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client: TestClient):
    # create a ToDo task, then transition to InProgress
    r = client.post("/tasks", json={"title": "transition ok"})
    assert r.status_code == 201
    task_id = r.json()["id"]

    r2 = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert r2.status_code == 200
    body = r2.json()
    assert body["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "transition bad"})
    assert r.status_code == 201
    task_id = r.json()["id"]

    r2 = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert r2.status_code == 422


def test_patch_same_status_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "same status"})
    assert r.status_code == 201
    task_id = r.json()["id"]

    # Current status is ToDo by default; setting ToDo again should return 422
    r2 = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert r2.status_code == 422


def test_delete_existing_returns_204_no_body(client: TestClient):
    r = client.post("/tasks", json={"title": "to delete"})
    assert r.status_code == 201
    task_id = r.json()["id"]

    r2 = client.delete(f"/tasks/{task_id}")
    assert r2.status_code == 204
    # per spec, 204 should have empty body
    assert r2.content == b""

    # subsequent GET should return 404
    r3 = client.get(f"/tasks/{task_id}")
    assert r3.status_code == 404


def test_delete_missing_returns_404(client: TestClient):
    fake_id = uuid.uuid4().hex
    r = client.delete(f"/tasks/{fake_id}")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == f"Task with id {fake_id} not found"
