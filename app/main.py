from fastapi import FastAPI
from fastapi import status
from app.models import TaskCreate, TaskResponse, TaskStatus, TaskPriority, TaskUpdate
from app import storage
from fastapi import HTTPException, status
from app.business_rules import validate_status_transition
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables from .env (optional)
load_dotenv()

app = FastAPI(
    title="Task Tracker API - Module 1",
    openapi_tags=[
        {"name": "system", "description": "Health and operational endpoints."},
        {"name": "tasks", "description": "Create, read, update, and delete tasks."},
    ],
)

# CORS: allow local frontend origins used during development
from fastapi.middleware.cors import CORSMiddleware
allowed_origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://0.0.0.0:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health", tags=["system"], summary="Service health check")
def health():
    """Health endpoint returning service status and current UTC timestamp in ISO format."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
    summary="Create a new task",
)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task from the provided payload and return the created task."""
    return storage.add_task(payload)


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    tags=["tasks"],
    summary="List tasks",
)
def list_tasks(status: TaskStatus | None = None, priority: TaskPriority | None = None) -> list[TaskResponse]:
    """Return a list of tasks. Optional query parameters: status and priority for filtering."""
    return storage.get_all_tasks(status=status, priority=priority)


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
    summary="Get task by id",
)
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by its id. Returns 404 if not found."""
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
    summary="Update a task (partial)",
)
def patch_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    # If status is provided, validate the transition against current task
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    updated = storage.update_task(task_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return updated


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
    summary="Delete a task",
)
def delete_task(task_id: str):
    deleted = storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return None


# Comments subresource
from app.comments import CommentCreate, CommentResponse, list_comments, add_comment, delete_comment


@app.get(
    "/tasks/{task_id}/comments",
    response_model=list[CommentResponse],
    tags=["tasks"],
    summary="List comments for a task",
)
def api_list_comments(task_id: str):
    """Return comments for the given task or 404 if the task does not exist."""
    return list_comments(task_id)


@app.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
    summary="Add a comment to a task",
)
def api_add_comment(task_id: str, payload: CommentCreate):
    """Create a comment for a task. Returns 404 if the task doesn't exist, 422 on validation."""
    return add_comment(task_id, payload)


@app.delete(
    "/tasks/{task_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
    summary="Delete a comment",
)
def api_delete_comment(task_id: str, comment_id: str):
    """Delete a comment; returns 404 if task or comment not found."""
    deleted = delete_comment(task_id, comment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Comment {comment_id} not found for task {task_id}")
    return None