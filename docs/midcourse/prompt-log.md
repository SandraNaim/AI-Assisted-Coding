
# Prompt Log — Search+Filters and Task Comments (strong prompts)

This log documents the prompts used to implement the two features in this mid-course project: Search & Combined Filters and Task Comments. For each feature I show:
- a strong prompt template (Context, Task, Constraints) that produced repeatable results,
- the AI's response summary,
- what I accepted, edited, or rejected,
- a weak→strong prompt rewrite example you can reuse.

Design note
The most reliable prompts contain 1) explicit context (base URL, exact endpoints, allowed enum values), 2) a concise task list, and 3) preservation constraints (what not to change). Asking for a focused diff or a single-file script replacement keeps the assistant's output small and reviewable.

---

## Feature: Search & Combined Filters — strong prompt

Context:
- Backend base URL: http://localhost:8000
- Endpoint to load tasks: GET /tasks
- Status values: ToDo, InProgress, Done
- Priority sort order inside each column: High, Medium, Low. Tie-breaker: id ascending.

Task:
- Extend `GET /tasks` to accept optional query params: `q` (text search over title+description), `status`, `priority`, `assignee`.
- Implement case-insensitive substring matching for `q` on title and description.
- Keep the API response shape unchanged (array of TaskResponse). Return 200 with [] when no matches.
- Add pytest tests for `q` search, combined filters, and invalid enum behavior (422).
- On the frontend, wire the filter/search bar to call `GET /tasks` with matching query params and re-render the board.

Constraints:
- Preserve column layout, empty placeholders, and existing class names.
- Do not add client-side-only filtering; the search must be server-side.
- Do not change backend request/response shapes beyond adding query params.
- Return a focused patch for the backend (one module) and a small frontend diff targeting the filter bar wiring.

What AI returned: Server-side filter code and helper `features.filter_tasks`, `GET /tasks` updated to accept query params, and frontend modifications to build the query string and call `fetchTasks(params)`. Tests scaffolding added.

---

## Feature: Task Comments — strong prompt

Context:
- Backend base URL: http://localhost:8000
- Comment endpoints should be mounted under: /tasks/{task_id}/comments

Task:
- Add a `CommentCreate` and `CommentResponse` Pydantic models.
- Add backend endpoints:
	- `GET /tasks/{task_id}/comments` — list comments for task (200 + [] when none, 404 if task missing).
	- `POST /tasks/{task_id}/comments` — create comment, require non-blank `text` (return 201 with created comment), 404 if task missing, 422 for validation.
	- `DELETE /tasks/{task_id}/comments/{comment_id}` — hard delete (204) or 404 if missing.
- Keep comments stored in a small in-memory dict (separate from Task storage) with optional JSON seed.
- Frontend: show comments only in the Edit Task modal (hide on New Task modal). Load comments when opening Edit (GET), allow add (POST) and delete (DELETE), and clear comments on modal close.

Constraints:
- Do not show per-card comment badges by default (comments are modal-only).
- Do not change existing task fields or the Task API shape.
- Return a focused backend module with models + storage helpers and the three endpoints, plus a small frontend modal change to toggle comments visibility and call endpoints.

What AI returned: `app/comments.py` with models and in-memory storage helpers, comments endpoints in `app/main.py`, and frontend wiring for modal-only comments (load, post, delete). Initial AI output included per-card badges and comments in the create modal which I removed.

---




