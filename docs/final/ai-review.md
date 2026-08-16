# AI review with human grading

Date: 2026-08-16
Branch: `final-project`
Single real changed file reviewed: `Dockerfile`

## Exact review input

I gave the AI the complete, real `Dockerfile` from this branch—not a
hypothetical example—and used this prompt:

> Review this Task Tracker Dockerfile for release reliability, security, and
> reproducibility. Give concrete comments tied to its actual lines. Do not
> assume every suggestion should be implemented. For each comment, explain the
> risk and a possible action.

The file supplied to the AI was:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data

RUN addgroup --system app && adduser --system --ingroup app app \
    && chown -R app:app /app

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

That is the real changed file immediately before applying the accepted health
check suggestion below. The current `Dockerfile` contains that resulting
change.

## AI comments and my grading

| Separate AI review comment | Grade | Why, what I verified, and my decision |
| --- | --- | --- |
| **1. "Add a container health check. The API has `/health`, but the image does not tell Docker how to use it."** | **Useful** | I checked `app/main.py` and confirmed that `GET /health` exists, returns `status: ok`, and has no dependency on task state. I checked the image base and avoided suggesting `curl`, which is not installed in `python:3.12-slim`. **Decision:** accepted. I added an exec-form `HEALTHCHECK` using Python's standard-library `urllib.request`. |
| **2. "Change Uvicorn from `--host 0.0.0.0` to `--host 127.0.0.1` to reduce network exposure."** | **Wrong** | I checked how Docker port publishing works. A process bound only to the container's loopback interface is not reachable through `docker run -p 8000:8000`. Binding to `0.0.0.0` inside the container is required for the documented host access; exposure is controlled when publishing the port. **Decision:** rejected and retained `0.0.0.0`. |
| **3. "Use a multi-stage build because every production Dockerfile should have one."** | **Noise** | I checked the build: there is no compiler toolchain, frontend build, or generated artifact to leave behind. Dependencies install directly into a slim Python runtime. A second stage would add complexity without a demonstrated size or security benefit for this project. **Decision:** rejected as an unrelated optimization. |
| **4. "Run the service as a non-root user instead of the image default."** | **Useful** | I checked the earlier Dockerfile revision and confirmed that it had no `USER` directive. The current file creates the system `app` user, gives it ownership of `/app`, and switches to it before startup. **Decision:** accepted before this captured review and retained after review. |

This provides four separate AI comments and includes all three required grades:
Useful, Noise, and Wrong.

## What I personally checked

I did not accept the proposed `127.0.0.1` binding merely because it sounded
more secure. I checked it against the actual Docker invocation documented in
the README (`-p 8000:8000`) and rejected it because it would make the container
unreachable from the host. This is the clearest example of independently
challenging AI output in this review.

I also checked the health implementation directly in `app/main.py` before
adding the Docker health check, and chose Python's standard library after
confirming the slim image does not guarantee a `curl` binary.

## Verification limitation

The Dockerfile change passed `git diff --check`. Building and running the image
is still blocked on this host because the current account cannot access
`/var/run/docker.sock`. Therefore this review records source verification and
the precise implementation decision, but does not claim an unobserved
container health result.
