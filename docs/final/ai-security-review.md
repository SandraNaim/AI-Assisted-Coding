# AI-assisted security review with human grading

Date: 2026-08-16
Scope: `Dockerfile`, `.dockerignore`, `.github/workflows/ci.yml`, `app/main.py`,
`.gitignore`, `.env.example`, and `frontend/index.html`.

The AI generated candidate security findings. I checked each candidate against
the named file and graded it rather than treating the output as authoritative.

| AI security finding | Grade | Supporting file and personal verification |
| --- | --- | --- |
| "The container runs as root because the Dockerfile has no `USER` directive." | Valid | The initial `Dockerfile` ended with `EXPOSE` and `CMD`. I confirmed there was no user change, then added a system `app` account and `USER app`. |
| "An API token may be exposed in the frontend because it contains the words `token-based auth`." | False Positive | The match is sample task description text in `frontend/index.html`, not a credential. I also searched tracked project content outside `.git`, `.venv`, and documentation for common key, secret, password, token, and private-key markers; no credential was found. |
| "The Docker build may copy `.env` secrets into the image." | False Positive | `.dockerignore` excludes `.env` and `.env.*`. More importantly, `Dockerfile` does not use `COPY . .`; it allowlists only `requirements.txt`, `app`, and `data`. `.env.example` contains only non-secret development settings and is not copied. |
| "CORS uses `allow_credentials=True`, so replace it immediately." | Noise | I checked `app/main.py`: origins are a fixed local-development allowlist, not `*`. The setting deserves reconsideration before public deployment, but changing it is outside this release exercise and no authentication credential is implemented. |
| "GitHub Actions should receive write-all permissions." | False Positive | `.github/workflows/ci.yml` only checks out code, installs dependencies, and runs pytest. It explicitly grants `contents: read`; no write permission is needed. |

## Secret and image-context checks

The repository check used a case-insensitive search for common secret markers
while excluding `.git`, `.venv`, and documentation. The only `token` match was
the non-secret placeholder sentence described above.

Image exclusion was checked at two layers:

1. `.dockerignore` excludes `.env` and every `.env.*` variant.
2. `Dockerfile` uses narrow `COPY` commands, so root-level environment files are
   outside the image even if the ignore file is accidentally weakened later.

A built-image filesystem inspection could not be completed because the host
denied access to `/var/run/docker.sock`. This record distinguishes source-level
verification from an actual image inspection.
