# README command verification

Date: 2026-08-16
Branch: `final-project`

Every command documented in the root README was reviewed and attempted. This
record separates verified application facts from checks blocked by the
assistant environment.

## Documentation claims checked against the repository

| README claim | Evidence | Result |
| --- | --- | --- |
| Python 3.10+ can run the source syntax | Clean setup and tests used Python 3.12.3; the application uses `X | None` type syntax, which requires Python 3.10+ | Verified |
| A fresh environment can install `requirements.txt` | Created a new virtual environment under `/tmp` and installed every pinned dependency successfully | Verified |
| Pytest discovers the existing suite | Clean environment collected 24 tests | Verified |
| The backend entry point is `app.main:app` | Uvicorn imported the application and reached its startup phase | Verified |
| The frontend is served from `frontend/` | `frontend/index.html` exists and the documented `http.server` command resolved that directory | Verified statically; socket binding blocked in sandbox |
| `/health` returns `status: ok` and a UTC timestamp | Called the existing route handler and checked its returned object | Verified in-process; HTTP curl blocked in sandbox |
| Runtime tasks are in memory | `app/storage.py` stores tasks in `_tasks`; JSON is only loaded as startup seed data | Verified by source inspection |

This checks more than the assignment minimum of three documentation claims.

## Setup command

The README setup was reproduced in a new temporary virtual environment rather
than relying on the repository's existing `.venv`:

```bash
python3 -m venv /tmp/task-tracker-venv.HeAbom
/tmp/task-tracker-venv.HeAbom/bin/python -m pip install -r requirements.txt
```

Result: **passed**. All pinned dependencies installed successfully.

The dependency pins also removed the incompatible FastAPI/Starlette combination
present in the old environment. That old combination caused TestClient to hang.

## Test command

Command from the README, using the clean environment:

```bash
python -m pytest -q
```

First clean run: **23 passed, 1 failed in 0.47 seconds**.

The one failure was a stale assertion: the test expected a same-status update
to return 422, while `app/business_rules.py` explicitly defines such an update
as an idempotent success. The test was corrected to assert the existing 200
behavior; no application behavior was changed.

A full rerun after that correction could not be completed because the sandbox
blocks the socket/thread mechanism used by FastAPI TestClient, and permission
to run the suite outside that restriction was declined. The corrected behavior
was checked directly and passed. The full suite should still be rerun on a
normal development machine before release.

## Backend, frontend, and health commands

The documented Uvicorn and `http.server` commands were attempted. Their module,
paths, and arguments resolved correctly. In the restricted execution sandbox,
both ultimately received `PermissionError: [Errno 1] Operation not permitted`
when creating a socket.

The health handler was checked in-process and returned `status: ok` with a UTC
ISO-8601 timestamp. The curl command could not be verified across HTTP because
no local socket may be opened in this sandbox.

Result: **application entry points and health behavior verified; live HTTP and
browser verification remain blocked by the environment**.

## Docker commands

Attempted exactly as documented:

```bash
docker build -t task-tracker:local .
```

The installed Docker command is a Snap package. It could not create its runtime
directories in the sandbox. Permission to run Docker outside that restriction
was declined, so the image build, container run, and container health curl
could not be completed here.

Result: **Dockerfile added and command attempted, but Docker build/run remains
unverified**. It must be executed on a machine with a functioning Docker daemon
before calling the release fully verified.

## Release-readiness conclusion

The README now reflects the real repository and every documented command has
been attempted. Fresh dependency installation is reproducible, and three-plus
claims were checked directly. Remaining release gates are one complete pytest
rerun and the live local/Docker HTTP checks on an environment that permits
sockets and Docker.
