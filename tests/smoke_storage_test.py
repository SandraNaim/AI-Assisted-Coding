from datetime import datetime, timezone
from app.models import TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from app import storage


def run_smoke():
    storage._reset()

    # Create
    payload = TaskCreate(title="  Test Task  ", description="desc")
    task = storage.add_task(payload)
    assert task.title == "Test Task"
    assert task.description == "desc"
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM

    # Get all
    all_tasks = storage.get_all_tasks()
    assert len(all_tasks) == 1

    # Get by id
    fetched = storage.get_task_by_id(task.id)
    assert fetched is not None
    assert fetched.id == task.id

    # Update
    upd = TaskUpdate(title=" Updated ", status=TaskStatus.IN_PROGRESS)
    updated = storage.update_task(task.id, upd)
    assert updated is not None
    assert updated.title == "Updated"
    assert updated.status == TaskStatus.IN_PROGRESS
    assert updated.updated_at >= updated.created_at

    # Delete
    deleted = storage.delete_task(task.id)
    assert deleted is True
    assert storage.get_task_by_id(task.id) is None

    # Validator: empty title
    try:
        TaskCreate(title="   ")
        raise SystemExit("Validator failed: blank title accepted")
    except Exception:
        pass

    print("SMOKE OK")


if __name__ == "__main__":
    run_smoke()
