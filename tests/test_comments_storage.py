from app import storage
from app.comments import _reset_comments, add_comment, list_comments, CommentCreate
from app.models import TaskCreate


def setup_function():
    storage._reset()
    _reset_comments()


def test_add_list_comment():
    task = storage.add_task(TaskCreate(title="T", description="", status="ToDo", priority="Medium", assignee=None))
    payload = CommentCreate(text="Nice job", author="bob")
    c = add_comment(task.id, payload)
    arr = list_comments(task.id)
    assert len(arr) == 1
    assert arr[0].text == "Nice job"
