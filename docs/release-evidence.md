# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-16
- Environment: Linux, Python 3.12.3
- Local app run command:

  ```bash
  python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
  ```

- `/health` result: the actual handler returned `status: ok` and a UTC
  timestamp in-process. Live HTTP was blocked because this sandbox denies local
  socket creation; HTTP `200 OK` still requires a normal local environment.
- Frontend check: `frontend/index.html` and its Kanban, modal, filters, and API
  wiring were inspected. Browser verification remains pending because of the
  same socket restriction.
- Test command:

  ```bash
  python -m pytest -q
  ```

- Test result:

  ```text
  ........................                                                 [100%]
  24 passed in 0.31s
  ```

The final suite was run in a clean temporary environment containing the exact
versions from `requirements.txt`.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: pending until `final-project` is pushed and the
  first workflow run completes.
- Test command used by CI: `python -m pytest -q`
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not
  skipped or filtered.
- Permissions: `contents: read`
- Job timeout: 10 minutes, so a hang fails visibly.

## Docker evidence

- Build command:

  ```bash
  docker build -t task-tracker:local .
  ```

- Run command:

  ```bash
  docker run --rm --name task-tracker -p 8000:8000 task-tracker:local
  ```

- `/health` check:

  ```bash
  curl --fail --show-error --write-out '%{http_code}\n' \
    http://127.0.0.1:8000/health
  ```

- Build result: blocked by host permissions. Direct Docker access returned
  `permission denied` for `/var/run/docker.sock`; `sudo -n docker build ...`
  returned `sudo: a password is required`.
- Docker `/health`: not observed because no image could be built or run. It
  must not be recorded as HTTP 200 until executed on a Docker-enabled account.
- Non-root check: `Dockerfile` creates a system `app` user and places
  `USER app` before `HEALTHCHECK` and `CMD`.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`, while
  Docker `COPY` instructions allowlist only `requirements.txt`, `app/`, and
  `data/`. A manual repository scan found no credential; built-image inspection
  remains pending.

Required built-image check:

```bash
docker run --rm task-tracker:local \
  sh -c 'find /app -name ".env" -o -name ".env.*"'
```

Expected output: empty.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
| --- | --- | --- | --- |
| Python 3.10+ can run the project | Source syntax and clean Python 3.12.3 environment | Verified | README now states Python 3.10+ and identifies 3.12 as verified. |
| A fresh setup can install dependencies | New temporary virtual environment installed all pinned requirements | Verified | Replaced unbounded minimum versions with tested exact versions. |
| `python -m pytest -q` runs the complete suite | Clean environment collected and ran 24 tests | Verified: 24 passed in 0.31s | Corrected one stale same-status assertion to match the existing idempotency rule. |
| Backend entry point is `app.main:app` | Uvicorn import/startup and direct handler smoke checks | Verified | README now uses the actual module entry point. |
| Frontend is under `frontend/` | Inspected `frontend/index.html` and its API base URL | Verified statically; browser pending | README now gives an explicit static-server command. |
| `/health` returns an OK payload | Called the actual `health()` handler | Verified in-process; HTTP pending | Added README curl command and Docker `HEALTHCHECK`. |
| Runtime task changes persist after restart | Inspected `_tasks` in `app/storage.py` and JSON seed loading | False; storage is in memory | README now says runtime changes are lost on restart. |
| Docker excludes environment secrets | Inspected `.dockerignore` and every Docker `COPY` target | Verified at source level; image inspection pending | Added `.env`/`.env.*` exclusions and narrow copy targets. |
| Docker build/run returns HTTP 200 | Attempted direct and non-interactive elevated builds | Not verified: host Docker permission blocked build | Recorded exact blocker and retained commands for a Docker-enabled machine. |
| GitHub Actions is successful | Workflow exists but has no observed remote run yet | Pending push/run | Added strict push and pull-request workflow. |

## Release status

Local automated tests are green. Remaining gates are Docker build/run HTTP 200,
manual browser/HTTP verification, pushing `final-project`, and recording the
successful GitHub Actions run link.
