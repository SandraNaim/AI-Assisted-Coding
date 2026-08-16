# Task Tracker

A small Kanban task tracker with a FastAPI backend and a static HTML,
CSS, and JavaScript frontend. Tasks move through `ToDo`, `InProgress`, and
`Done`. The API also supports task creation, editing, deletion, search, and
filtering.

Tasks are held in memory while the backend is running. `data/tasks.json` may
seed tasks at startup, but runtime changes are lost when the backend stops.

## Requirements

- Python 3.10 or newer (Python 3.12 is used for the verified setup)
- Docker, only if using the Docker instructions

## Local setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the backend

With the virtual environment activated, run:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation
is available at `http://127.0.0.1:8000/docs`.

Keep this terminal running while using the frontend.

## Run the frontend

Open a second terminal in the repository root, activate the virtual
environment, and run:

```bash
python -m http.server 8080 --bind 127.0.0.1 --directory frontend
```

Open `http://127.0.0.1:8080` in a browser. The frontend expects the backend at
`http://localhost:8000`, so the backend must also be running on port 8000.

## Verify the health endpoint

With the backend running:

```bash
curl --fail --show-error http://127.0.0.1:8000/health
```

The response contains an `ok` status and a UTC timestamp, for example:

```json
{"status":"ok","timestamp":"2026-08-16T08:49:26.987692+00:00"}
```

## Run the tests

With the virtual environment activated:

```bash
python -m pytest -q
```

Pytest discovers the test suite under `tests/` and exits with a nonzero status
if a test fails.

## Build and run with Docker

The Docker image runs the backend API. From the repository root:

```bash
docker build -t task-tracker:local .
docker run --rm --name task-tracker -p 8000:8000 task-tracker:local
```

In a second terminal, verify the container:

```bash
curl --fail --show-error http://127.0.0.1:8000/health
```

Stop the foreground container with `Ctrl+C`. The frontend remains a static
site and can be run with the local frontend command above while the backend is
in Docker.

## API summary

- `GET /health` checks service health.
- `POST /tasks` creates a task.
- `GET /tasks` lists and filters tasks.
- `GET /tasks/{task_id}` returns one task.
- `PATCH /tasks/{task_id}` updates a task.
- `DELETE /tasks/{task_id}` deletes a task.

## Verification record

Final-project verification evidence, including commands, results, and any
environment limitations, is recorded under `docs/final/`.

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker remains inside the intended course scope.
- CI runs the complete pytest suite on pushes and pull requests without masking
  failures.
- The Docker image is configured to run as a non-root user and check `/health`.
- AI review, security review, verification, and ownership evidence are in
  `docs/`.

Observed pass/fail evidence is recorded in `docs/release-evidence.md`; a check
is not described as successful there until it has actually run.

### How to run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal:

```bash
source .venv/bin/activate
python -m http.server 8080 --bind 127.0.0.1 --directory frontend
```

Open `http://127.0.0.1:8080`.

### How to run tests

```bash
source .venv/bin/activate
python -m pytest -q
```

### How to run with Docker

```bash
docker build -t task-tracker:local .
docker run --rm --name task-tracker -p 8000:8000 task-tracker:local
```

In a second terminal:

```bash
curl --fail --show-error --write-out '%{http_code}\n' \
  http://127.0.0.1:8000/health
```

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI assistance summary

AI helped draft and review CI, Docker, documentation, security findings, and
dependency debugging. I verified the work through clean-environment installs,
tests, diff review, source inspection, secret scanning, and health checks where
the environment allowed them. I rejected the suggestion to bind Uvicorn to
`127.0.0.1` inside Docker because it would break published-port access, and I
corrected a stale same-status test after checking the actual business rule.
