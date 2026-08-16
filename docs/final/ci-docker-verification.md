# CI and Docker verification

Date: 2026-08-16
Branch: `final-project`

## GitHub Actions

`.github/workflows/ci.yml` runs on both `push` and `pull_request`, uses Python
3.12, installs the pinned requirements, and runs:

```bash
python -m pytest -q
```

The workflow has no `continue-on-error`, `|| true`, test selection, or skipped
test path. Its token permission is limited to `contents: read`, and the job has
a 10-minute timeout so a hang fails visibly.

The same pinned installation was tested in a fresh local virtual environment.
It installed successfully. Its first suite run completed with 23 passes and one
stale assertion; that assertion was reconciled against the existing business
rule and corrected. A final unrestricted rerun was requested but declined, and
the restricted sandbox cannot execute FastAPI TestClient requests. The first
GitHub Actions run will therefore be the authoritative complete
post-correction result.

## Docker source checks

The Docker configuration now:

- starts from `python:3.12-slim`;
- installs the same pinned `requirements.txt` used by CI;
- copies only `app/` and `data/` as runtime content;
- runs as an unprivileged `app` user;
- exposes port 8000 and starts `app.main:app` on `0.0.0.0:8000`;
- defines a Docker health check against the existing `/health` endpoint using
  Python's standard library;
- excludes Git data, virtual environments, tests, docs, frontend files, `.env`,
  and `.env.*` from the build context.

## Docker build/run/health attempt

Build command:

```bash
docker build -t task-tracker:local .
```

Result: **blocked by host permissions**:

```text
permission denied while trying to connect to the docker API at
unix:///var/run/docker.sock
```

Because no image was built, running the container and claiming an HTTP 200 from
its `/health` endpoint would be misleading. These commands remain mandatory on
a Docker-enabled machine:

```bash
docker build -t task-tracker:local .
docker run --rm --name task-tracker -p 8000:8000 task-tracker:local
curl --fail --show-error --write-out '%{http_code}\n' \
  http://127.0.0.1:8000/health
```

Expected curl status: `200`. Then inspect the built filesystem explicitly:

```bash
docker run --rm task-tracker:local \
  sh -c 'find /app -name ".env" -o -name ".env.*"'
```

Expected output: empty. Source-level inspection already confirms those files
are not copy targets, but this final runtime check must be captured before the
Docker verification is marked complete.
