from __future__ import annotations

from typing import Optional, List, Dict
from datetime import datetime, timezone
from uuid import uuid4

from .models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority
import json
from pathlib import Path

# In-memory storage
_tasks: Dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """
    Create a new TaskResponse from TaskCreate and store it in _tasks.
    """
    task_id = uuid4().hex
    now = datetime.now(timezone.utc)
    data = payload.model_dump()
    data.update({"id": task_id, "created_at": now, "updated_at": now})
    task = TaskResponse(**data)
    _tasks[task_id] = task
    return task


def get_all_tasks(status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None) -> List[TaskResponse]:
    """
    Return all tasks, optionally filtered by status and/or priority.
    """
    results: List[TaskResponse] = []
    for task in _tasks.values():
        if status is not None and task.status != status:
            continue
        if priority is not None and task.priority != priority:
            continue
        results.append(task)
    return results


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """
    Return a task by id or None if not found.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """
    Update an existing task with fields from payload (using model_dump(exclude_unset=True)).
    Returns the updated TaskResponse or None if not found.
    """
    existing = _tasks.get(task_id)
    if existing is None:
        return None

    existing_data = existing.model_dump()
    patch = payload.model_dump(exclude_unset=True)

    # Merge patch into existing data
    updated_data = {**existing_data, **patch}
    updated_data["updated_at"] = datetime.now(timezone.utc)

    updated_task = TaskResponse(**updated_data)
    _tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: str) -> bool:
    """
    Delete a task by id. Return True if deleted, False if not found.
    """
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    """
    Clear all tasks (for tests only).
    """
    _tasks.clear()


# Seed in-memory store from data/tasks.json (development convenience)
def _load_seed_from_file():
    try:
        seed_path = Path(__file__).resolve().parents[1] / 'data' / 'tasks.json'
        if not seed_path.exists():
            return
        raw = seed_path.read_text(encoding='utf-8')
        items = json.loads(raw)
        # only populate when storage is empty
        if not items or _tasks:
            return
        for item in items:
            try:
                # Build TaskCreate-like dict and use add_task for consistent IDs/timestamps
                tc = TaskCreate(
                    title=item.get('title', ''),
                    description=item.get('description', ''),
                    status=TaskStatus(item.get('status', 'ToDo')),
                    priority=TaskPriority(item.get('priority', 'Medium')),
                    assignee=item.get('assignee', None),
                )
                add_task(tc)
            except Exception:
                # skip malformed seed items
                continue
    except Exception:
        # non-fatal; fail silently to avoid crashing app on import
        return


# Load seeds at import time (if present)
_load_seed_from_file()