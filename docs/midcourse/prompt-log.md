# Prompt Log — Search/Filters and Modal-only Comments

This log records the meaningful prompts used while implementing the two features. For each prompt, I summarize the AI response and note whether I accepted, edited, or rejected the result.

## Feature: Search & Combined Filters

Prompt 1 (initial, weak):
"Add a search box to the frontend and make the backend support searching tasks."
- AI returned: high-level plan suggesting client-side filtering and optional server indexes.
- Action: Rewrote prompt to require server-side filtering and precise query param names; rejected the client-only approach.

Prompt 2 (stronger):
"Implement server-side GET /tasks?q= to search title+description and also accept status, priority, assignee as query params. Use simple substring matching for q and enum validation for status/priority. Add tests."
- AI returned: code patches for `app/features.py`, changes to `GET /tasks` in `app/main.py`, and frontend wiring.
- Action: Accepted with small edits to validation messages and adapted frontend querystring building.

Prompt 3 (test prompt):
"Write pytest test cases for GET /tasks filters: q-only, combined filters, invalid enum should return 422."
- AI returned: pytest files using FastAPI TestClient.
- Action: Accepted tests; could not run locally here (pytest missing) so marked for local verification.

## Feature: Modal-only Comments

Prompt 1 (initial):
"Add comments to tasks: list, create, delete. Show comment counts on cards and a comment input on the task modal."
- AI returned: code to embed comments on cards and show comment inputs on both Create and Edit modals.
- Action: Rejected parts: I removed per-card counts and kept comments modal-only and edit-only.

Prompt 2 (refined):
"Make comments a subresource under /tasks/{task_id}/comments with GET, POST, DELETE, and validate non-blank text. In the frontend, only show comments in the Edit modal (hide in New Task modal)."
- AI returned: `app/comments.py`, endpoints in `app/main.py`, frontend wiring for modal-only comments.
- Action: Accepted, then tweaked UI to ensure comments section is hidden for New Task and shown for Edit.

Prompt 3 (improvement):
"Fix the frontend so that, on the Create modal, the comments section is not visible; on Edit, show and load comments. Also on modal close the comments list should be cleared."
- AI returned: JS changes to `openModalCreate`, `openModalEdit`, and `closeModal` to toggle visibility and call `loadComments` appropriately.
- Action: Accepted and committed.

### Rewritten (improved) prompt example
Weak prompt: "Add comments to tasks."
Stronger replacement I used: "Implement a comments subresource mounted at `/tasks/{task_id}/comments` with `GET` (list), `POST` (create, requires non-blank `text`), and `DELETE` (delete by id). Update frontend so comments are only available when editing an existing task: hide comments in New Task modal and show/load comments in Edit modal. Return 201 for create, 204 for delete, 404 for missing task/comment, and 422 for validation errors."
- AI returned: specific code changes and tests. I accepted the overall approach and edited the UI behavior to remove per-card badges.

