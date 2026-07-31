import json
import os
from typing import Any, List
from filelock import FileLock

DEFAULT_PATH = os.path.join("data", "tasks.json")

def init_storage(path: str = DEFAULT_PATH) -> None:
    """
    Ensure the data directory and tasks file exist.
    """
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)

def load_tasks(path: str = DEFAULT_PATH) -> List[Any]:
    """
    Load and return the list of tasks from the JSON file.
    """
    init_storage(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks: List[Any], path: str = DEFAULT_PATH) -> None:
    """
    Atomically write the tasks list to disk using a temporary file and file lock.
    """
    init_storage(path)
    lock_path = path + ".lock"
    tmp_path = path + ".tmp"
    with FileLock(lock_path):
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)