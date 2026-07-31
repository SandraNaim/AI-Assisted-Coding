import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import storage


@pytest.fixture(autouse=True)
def _reset_storage():
    # Ensure storage is clean before and after each test
    storage._reset()
    try:
        yield
    finally:
        storage._reset()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_task(client: TestClient):
    r = client.post("/tasks", json={"title": "fixture task"})
    assert r.status_code == 201
    return r.json()
