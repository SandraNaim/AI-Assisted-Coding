# Final project baseline verification

Date: 2026-08-16
Branch: `final-project`
Environment: Linux, Python 3.12.3

This baseline was recorded before making any application changes. Its purpose is
to preserve the existing behavior and report failures honestly, not to add new
features.

## Repository state

Commands:

```bash
git status --short --branch
git switch -c final-project
```

Result:

- The starting branch was `mid-course-project` and the worktree was clean.
- The new `final-project` branch was created successfully.
- No application files were changed before the checks below.

## Existing automated test suite

Command:

```bash
.venv/bin/python -m pytest -q
```

Result: **inconclusive / needs investigation**. Pytest did not finish.

A verbose, time-bounded reproduction was used:

```bash
timeout 60s .venv/bin/python -m pytest -vv
```

Pytest collected 24 tests, then stopped making progress at:

```text
tests/test_comments_api.py::test_comments_create_list_delete_flow
```

The command exited with status 124 after the 60-second timeout. This is a
release-readiness blocker until it is determined whether the cause is the test
environment, dependency compatibility, or application behavior.

The storage-only checks were also isolated:

```bash
timeout 20s .venv/bin/python -m pytest -q \
  tests/smoke_storage_test.py tests/test_comments_storage.py
```

Result: **1 passed** in 0.02 seconds, with one deprecation warning from the
installed FastAPI/Starlette TestClient compatibility layer.

## Backend startup and health check

Command:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010
```

Uvicorn reported successful application startup and listening on
`http://127.0.0.1:8010`.

Attempted check:

```bash
curl --max-time 5 -i http://127.0.0.1:8010/health
```

Result: **not verified over HTTP in the assistant sandbox**. The sandbox did
not permit the curl process to connect to the loopback server, even though
Uvicorn reported that it was running. The same restriction occurred with the
frontend server. This environment limitation must not be recorded as an
application pass.

As a limited in-process smoke check, the `health()` route handler returned:

```text
{'status': 'ok', 'timestamp': '<UTC ISO-8601 timestamp>'}
```

## Existing task flow

The route handlers were exercised in-process without modifying the source:

1. Create a task with the default `ToDo` status.
2. Edit its status to `InProgress`.
3. List tasks and confirm one task is present.
4. Delete it and confirm the list is empty.

Result: **passed as an in-process smoke check**.

This does not replace the blocked HTTP/browser verification. A developer should
repeat the following locally before release:

```bash
.venv/bin/uvicorn app.main:app --reload --port 8000
.venv/bin/python -m http.server 8080 --directory frontend
curl -i http://127.0.0.1:8000/health
```

Then open `http://127.0.0.1:8080`, create a task, edit it, and move it through
the normal Kanban workflow.

## Frontend baseline

The static frontend server command was started:

```bash
.venv/bin/python -m http.server 8080 --bind 127.0.0.1 --directory frontend
```

The server process started, but an HTTP request could not cross the sandbox's
loopback restriction. Static inspection confirmed that `frontend/index.html`
exists and contains the current Kanban board, New Task control, edit modal,
filter controls, and task API request wiring.

Result: **files present; browser interaction still requires local manual
verification**.

## Baseline conclusion

The core storage operations and in-process task flow work, and both server
commands start. The project cannot yet be called release-ready because the full
test suite hangs and real HTTP/browser checks remain unverified in this
environment. No new product features should be added while resolving these
baseline issues.
