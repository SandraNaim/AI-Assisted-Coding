# Task Tracker — Module 1 (FastAPI)

Minimal learning-project skeleton for the Task Tracker REST API (Module 1). This project uses FastAPI and a simple JSON file for local storage so you can focus on API design and frontend integration.

## What's included

- `app/main.py` — FastAPI app with a `/health` endpoint
- `app/models.py` — Pydantic model sketches for tasks (for future use)
- `app/storage/json_storage.py` — simple file-based helpers to read/write `data/tasks.json`
- `data/tasks.json` — initial empty array
- `requirements.txt` — project dependencies
- `.env.example` — example environment variables
- `.gitignore` — sensible Python ignores

## Requirements

- Python 3.9+ (3.10+ recommended)

## Setup (Linux / macOS)

```bash
# create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt