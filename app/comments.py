from __future__ import annotations

from typing import Optional, Dict, List
from datetime import datetime, timezone
from uuid import uuid4
from pathlib import Path
import json

from pydantic import BaseModel, ConfigDict, field_validator
from fastapi import HTTPException, status

from app import storage


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    author: Optional[str] = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if v is None:
            raise ValueError("text is required")
        v2 = v.strip()
        if len(v2) == 0:
            raise ValueError("text must not be blank")
        return v2


class CommentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    text: str
    author: Optional[str]
    created_at: datetime


# In-memory comments store: task_id -> (comment_id -> CommentResponse)
_comments: Dict[str, Dict[str, CommentResponse]] = {}


def list_comments(task_id: str) -> List[CommentResponse]:
    """Return comments for a task ordered by created_at ascending.

    Raises 404 if the task does not exist.
    """
    if storage.get_task_by_id(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    mapping = _comments.get(task_id, {})
    return sorted(list(mapping.values()), key=lambda c: c.created_at)


def add_comment(task_id: str, payload: CommentCreate) -> CommentResponse:
    """Add a comment to a task and return the created CommentResponse.

    Raises 404 if the task does not exist. Validation of `text` is handled by Pydantic.
    """
    if storage.get_task_by_id(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")

    cid = uuid4().hex
    now = datetime.now(timezone.utc)
    data = payload.model_dump()
    data.update({"id": cid, "created_at": now})
    comment = CommentResponse(**data)
    _comments.setdefault(task_id, {})[cid] = comment
    return comment


def delete_comment(task_id: str, comment_id: str) -> bool:
    """Delete a comment. Return True if deleted, False if not found.

    Raises 404 if the task does not exist.
    """
    if storage.get_task_by_id(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    bucket = _comments.get(task_id)
    if not bucket:
        return False
    return bucket.pop(comment_id, None) is not None


def _reset_comments() -> None:
    """Clear all comments (for tests)."""
    _comments.clear()


# Optional: load seed comments from data/comments.json at import time (non-fatal)
def _load_seed_from_file() -> None:
    try:
        seed_path = Path(__file__).resolve().parents[1] / 'data' / 'comments.json'
        if not seed_path.exists():
            return
        raw = seed_path.read_text(encoding='utf-8')
        items = json.loads(raw)
        if not isinstance(items, list):
            return
        for it in items:
            try:
                tid = it.get('task_id')
                if not tid:
                    continue
                # Skip if task missing
                if storage.get_task_by_id(tid) is None:
                    continue
                payload = CommentCreate(text=it.get('text', ''), author=it.get('author'))
                add_comment(tid, payload)
            except Exception:
                continue
    except Exception:
        return


_load_seed_from_file()
