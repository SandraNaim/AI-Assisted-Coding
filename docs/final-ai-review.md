# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: **yes**
- Docs-first/read-first guardrail included: **yes**
- Unexpected app/frontend edits rule included: **yes** — agents must preserve
  scope, avoid unrelated UI work, make the smallest relevant change, and stop
  before adding authentication, notifications, databases, or new comment work.

I read the final root `AGENTS.md` and checked each answer against its actual
text rather than assuming the file name alone satisfied the requirement.

## AI code review mini-log

Real changed file reviewed: `Dockerfile`

Prompt given to AI:

> Review this Task Tracker Dockerfile for release reliability, security, and
> reproducibility. Give concrete comments tied to its actual lines. Do not
> assume every suggestion should be implemented. For each comment, explain the
> risk and a possible action.

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
| --- | --- | --- | --- |
| Add a Docker health check using the existing `/health` route. | **Useful** | The image otherwise gives Docker no native health signal. | Verified `/health` in `app/main.py`; accepted using Python `urllib.request` because the slim image does not guarantee `curl`. |
| Bind Uvicorn to `127.0.0.1` inside the container. | **Wrong** | Container loopback binding would prevent access through the documented published port. | Checked Docker networking behavior; rejected and retained `0.0.0.0`. |
| Use a multi-stage build because every production Dockerfile should. | **Noise** | There is no compiler toolchain, frontend build, or generated artifact to remove. | Inspected all build steps; rejected unsupported complexity. |
| Run the container as a non-root user. | **Useful** | The initial file relied on the base image's root user. | Confirmed the missing `USER`, added system user `app`, and retained `USER app`. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
| --- | --- | --- | --- | --- |
| Initial container runs as root. | Initial `Dockerfile` had no `USER`. | **Valid** | Default root increases impact if the service is compromised. | Fixed by creating and switching to unprivileged `app`. |
| An API token is exposed in frontend text. | `frontend/index.html` contains the phrase `token-based auth`. | **False Positive** | It is placeholder task prose, not a credential. | No code change; retained repository secret scanning. |
| `.env` secrets may be copied into the image. | `.dockerignore` excludes `.env`/`.env.*`; `Dockerfile` uses narrow `COPY` targets. | **False Positive** | Neither `.env` nor `.env.example` is a copy target. | Run the documented built-image `find` command when Docker access is available. |
| CORS credentials must be removed immediately. | `app/main.py` has `allow_credentials=True` with fixed localhost origins. | **Noise** | It is worth reassessing for deployment, but origins are not wildcarded and this app has no authentication credentials. | Record as a future deployment review item; do not expand final-project scope. |

## Manual security check

I searched repository content outside `.git`, `.venv`, and documentation for
common API-key, secret, password, token, and private-key markers. The only token
match was the non-secret placeholder sentence above. I also traced every Docker
`COPY` instruction and confirmed that environment files, Git history, tests,
and documentation are not copied into the runtime image. This matters because
`.dockerignore` alone should not be the only defense against baking secrets
into an image.

## One AI output I rejected or corrected

AI suggested binding Uvicorn to `127.0.0.1` inside Docker as a security
improvement. I did not accept it because checking the documented
`-p 8000:8000` workflow showed that container-loopback binding would make the
API unreachable from the host. I retained `0.0.0.0` and rely on Docker port
publishing to control host exposure. I also corrected a stale test expectation
instead of changing the explicit idempotent transition rule merely to get a
green test.

## Three AI usage rules

1. **Never paste:** credentials, tokens, private keys, customer data, or real
   private `.env` contents.
2. **Always verify:** compare suggestions with source and scope, inspect the
   whole diff, and run every command before recording it as successful.
3. **Record AI contributions by:** naming the reviewed file or diff, preserving
   concrete comments, grading them, and documenting accepted, rejected, or
   corrected output.

## Ownership statement

I used AI to accelerate review, documentation, dependency debugging, and small
release-readiness changes, but I treated every output as a proposal. I checked
the status-transition implementation myself and corrected the test rather than
changing intentional behavior. I rejected a plausible Docker recommendation
after verifying that it would break published-port access. I am comfortable
submitting this work because I can explain the accepted changes and have
clearly recorded the remaining Docker and remote-CI evidence instead of
inventing results.
