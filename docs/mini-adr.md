# Mini-ADR: Implementing Search+Filters and Task Comments (lightweight)

Date: 2026-07-31
Status: Accepted

## Context
We are extending the Task Tracker (FastAPI backend + simple frontend) to support two features:

1. Text search and combined filters on tasks (q, status, priority, assignee, optional tag/due_date).
2. Task comments as a subresource (list/add/delete) with non-blank validation.

Constraints: learning project, single-process local dev, no auth, use Python/FastAPI/Pydantic, keep stack minimal and easy to run.

## Decision
- Implement search and combined filters in the existing GET /tasks handler via query parameters. Use case-insensitive substring matching for `q` and strict enum validation for `status` and `priority`.
- Implement comments as a new subresource with endpoints under `/tasks/{task_id}/comments`. Store comments in-memory and support optional seeding from `data/comments.json`.
- Use Pydantic models for validation (CommentCreate, CommentResponse), and re-use existing Task models for consistency.
- Keep persistence lightweight: in-memory dictionaries for runtime; optional JSON seed files for developer convenience.

## Alternatives considered and rejected
- Full-text indexing (SQLite FTS or external search): rejected for now because it adds infrastructure complexity; substring matching is adequate for the dataset sizes expected in a learning project.
- Storing comments inline inside Task objects: rejected because a subresource API (separate collection) makes listing, adding, and deleting simpler and keeps the Task model focused.
- Using a production DB (Postgres/managed services): out of scope for the learning constraints.

## Data model (sketch)
- CommentCreate (Pydantic):
  - text: str (required, non-blank)
  - author: Optional[str]
- CommentResponse (Pydantic):
  - id: str (uuid4.hex)
  - text: str
  - author: Optional[str]
  - created_at: datetime (UTC)

Storage runtime shape (app.storage):
- _comments: dict[task_id:str, dict[comment_id:str, CommentResponse]]

## API endpoints (sketch)
- GET /tasks?q=&status=&priority=&assignee=&tag=&due_date=
  - 200 OK with list of TaskResponse; 200 + [] if no matches; 422 for invalid enum or invalid due_date format.
- GET /tasks/{task_id}/comments
  - 200 + [] if no comments; 404 if task not found.
- POST /tasks/{task_id}/comments
  - 201 Created with CommentResponse; 422 for blank text; 404 if task not found.
- DELETE /tasks/{task_id}/comments/{comment_id}
  - 204 No Content; 404 if task or comment not found.

## Validation & Errors
- Use Pydantic validators to enforce non-blank text for comments and to coerce/validate enums for filters.
- Return standard FastAPI 422 for validation errors and 404 for missing resources.

## Testing & Verification
- Unit tests for storage helpers: list/add/delete comments.
- Integration tests (pytest + TestClient) for endpoints:
  - search queries: q-only, combined filters, no-results, invalid enum value.
  - comments: create (201), create blank (422), list (200), delete (204), delete missing (404).

## Migration & developer UX
- Provide `data/comments.json` as an optional seed file.
- Implement `_load_seed_from_file()` in `app.storage` to populate comments at startup if present (non-fatal if missing).
- Add `scripts/export_data.py` (optional) to dump runtime state to `data/*.json` for manual persistence between runs.

## Implementation plan (minimal phases)
1. Add Pydantic Comment models and storage functions.
2. Add comments endpoints to `app/main.py` with OpenAPI docs and tests.
3. Extend GET /tasks to accept `q` and other filters; add tests and UI wiring.
4. Add seed file examples and README updates.

## Notes
- This ADR is intentionally lightweight: focused on an educational, easy-to-run setup. When the project needs to scale, migrate to SQLite (or similar) and consider adding simple FTS or indexed queries.

---

Signed-off-by: product owner / senior backend developer (notes for the team)
