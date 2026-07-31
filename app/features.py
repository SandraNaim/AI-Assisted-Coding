from __future__ import annotations

from typing import Iterable, List, Optional
from datetime import datetime

from app.models import TaskResponse, TaskStatus, TaskPriority


def _match_text(task: TaskResponse, q: str) -> bool:
    ql = q.lower()
    return (ql in (task.title or '').lower()) or (ql in (task.description or '').lower())


def _match_status(task: TaskResponse, status: TaskStatus) -> bool:
    return task.status == status


def _match_priority(task: TaskResponse, priority: TaskPriority) -> bool:
    return task.priority == priority


def _match_assignee(task: TaskResponse, assignee: str) -> bool:
    if assignee is None or assignee == '':
        return True
    return (task.assignee or '') == assignee


def filter_tasks(
    tasks: Iterable[TaskResponse],
    q: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None,
    due_date: Optional[str] = None,  # optional format YYYY-MM-DD, parsing is caller's responsibility
    tag: Optional[str] = None,  # optional; tasks may include tags in future
) -> List[TaskResponse]:
    """Return tasks that match all provided filters (AND semantics)."""
    out: List[TaskResponse] = []
    for t in tasks:
        if q is not None and q.strip() != '':
            if not _match_text(t, q):
                continue
        if status is not None and not _match_status(t, status):
            continue
        if priority is not None and not _match_priority(t, priority):
            continue
        if assignee is not None and assignee.strip() != '' and not _match_assignee(t, assignee):
            continue
        # due_date and tag are no-ops here; caller may implement parsing or extend TaskResponse
        out.append(t)
    return out
