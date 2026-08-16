# Instructions for AI coding agents

## Project and stack

This repository is a small learning-focused Task Tracker. The backend is
Python 3.10+ with FastAPI and Pydantic. The frontend is one static
`frontend/index.html` file using plain HTML, CSS, and JavaScript. Tasks and
comments are stored in memory; `data/tasks.json` is startup seed data, not a
production database.

Read `README.md`, existing source, tests, and relevant `docs/` files before
changing anything. Treat current business rules as intentional until they are
checked against both implementation and tests.

## Setup and commands

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
python -m http.server 8080 --bind 127.0.0.1 --directory frontend
```

Docker verification:

```bash
docker build -t task-tracker:local .
docker run --rm --name task-tracker -p 8000:8000 task-tracker:local
curl --fail --show-error http://127.0.0.1:8000/health
```

## Working rules

1. Inspect the existing implementation, tests, README, and final-project
   evidence before proposing a change.
2. Preserve scope. Do not add authentication, notifications, a production
   database, new comment functionality, or unrelated UI changes.
3. Prefer release-readiness work: reproducible setup, tests, CI, Docker,
   security checks, and accurate documentation.
4. Never weaken, skip, or hide a failing test. Do not use `continue-on-error`,
   `|| true`, or remove coverage merely to make CI green.
5. Do not change application behavior just to satisfy a stale test. Compare the
   test with the documented and implemented business rule, then record the
   decision.
6. Never paste, log, commit, or invent secrets. Keep `.env` files outside Git
   and the Docker image.
7. Make the smallest relevant change and avoid opportunistic refactors.
8. Run every command added to documentation. If the environment blocks a
   command, record the exact limitation instead of claiming success.
9. Before finishing, run `git diff --check`, the complete test suite, and the
   relevant health checks whenever the environment permits them.

## Evidence requirements

Keep `docs/release-evidence.md`, `docs/final-ai-review.md`, and
`docs/ai-playbook.md` accurate. Separate observed results from expected results.
Never label GitHub Actions, Docker, tests, or HTTP checks successful without
direct evidence.
