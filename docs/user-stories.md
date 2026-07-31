# User stories: Search & Combined Filters, Task Comments

This document contains user stories (3–5 per feature) drawn from the project planning session. Each story includes specific, testable acceptance criteria and notes about AI assumptions that were corrected.

## Feature: Search & Combined Filters

Story 1
- As a team member, I want text search on tasks (title + description) so that I can quickly find relevant tasks.

Acceptance criteria
- GET /tasks?q=term returns 200 and only tasks where title or description contains "term" (case-insensitive).
- Omitted or empty `q` behaves like no-filter and returns 200 with all tasks.
- Search results update board columns and counts to reflect returned tasks.

AI assumption corrected
- AI initially proposed full-text indexing (FTS). For this learning project we decided to use simple case-insensitive substring matching to keep the stack minimal.

Story 2
- As a team member, I want to combine filters (status, priority, assignee) so that I can narrow results precisely.

Acceptance criteria
- GET /tasks?status=InProgress&priority=High&assignee=maya returns 200 and only tasks matching all provided filters.
- If no tasks match the combination, API returns 200 with an empty array and frontend shows empty columns (visible) and zero counts.
- If a filter value is syntactically invalid (e.g., status=BadValue) the API returns 422 with a clear error message; the UI surfaces that message.

AI assumption corrected
- AI suggested implicit loose parsing of filter values; we chose strict validation using existing enums (status/priority) to keep behavior predictable.

Story 3
- As a team member, I want a compact filter + search bar above the board so that I can run quick queries without leaving the main view.

Acceptance criteria
- The bar is visible above the board and contains a free-text search field plus compact controls for status, priority, and assignee.
- Submitting the bar issues a single GET /tasks request with matching query params; board columns remain visible and counts update based on the response.
- If the server returns 422, the bar shows the server error message in-line and does not break the board layout.

AI assumption corrected
- AI initially considered hiding columns on filtered view; we decided to always keep columns visible and show empty placeholders to maintain consistent UX.

Story 4 (optional extension)
- As a team member, I want combined filters to optionally include tag and due-date if supported by the backend so that advanced filtering works when available.

Acceptance criteria
- If backend supports `tag` or `due_date`, GET /tasks?tag=foo or GET /tasks?due_date=YYYY-MM-DD returns 200 and filters results accordingly.
- If frontend supplies a due_date in invalid format, and backend validates it, API returns 422 and UI surfaces the validation message.
- If backend does not expose tag/due_date, providing those params is ignored (or returns 422 per backend design) and UI handles either case gracefully (error shown or ignored).

AI assumption corrected
- AI had suggested always implementing due_date parsing; we mark this as optional and frontend must be tolerant if backend does not implement it.

---

## Feature: Task Comments

Story 1
- As a team member, I want to list comments for a task so I can read existing discussion before editing.

Acceptance criteria
- GET /tasks/{task_id}/comments returns 200 with a JSON array of comments for that task, each having id, text, author (optional), created_at.
- Comments are ordered by created_at ascending (oldest first).
- If task_id does not exist, API returns 404 and UI displays a 'Task not found' message in the modal/detail view.

AI assumption corrected
- AI proposed comments as an embedded free-form field; we decided to implement comments as a first-class subresource to keep API RESTful and easier to manage.

Story 2
- As a team member, I want to add a comment to a task so that I can leave notes or context for others.

Acceptance criteria
- POST /tasks/{task_id}/comments with JSON { "text": "..." } returns 201 and the created comment payload (id, text, author?, created_at).
- Sending a blank or whitespace-only `text` returns 422 with a validation message and the comment is not created.
- If task_id does not exist, POST returns 404.

AI assumption corrected
- AI suggested optional author auto-fill; for simplicity we keep author optional and let clients provide it or leave null.

Story 3
- As a team member, I want to delete a comment so that I can remove obsolete or mistaken notes.

Acceptance criteria
- DELETE /tasks/{task_id}/comments/{comment_id} returns 204 on success and subsequent GET /tasks/{task_id}/comments does not include the deleted comment.
- If task_id or comment_id does not exist, API returns 404 and UI shows an appropriate error message.
- Card UI (optional) shows an updated comment count after add/delete operations.

AI assumption corrected
- AI suggested soft-delete; we decided to implement hard delete for simplicity in a learning project.

---

### Notes
- Each story is intentionally small and testable. The backend will use FastAPI and Pydantic for validation; persistence remains in-memory with optional JSON seeding to keep the environment simple for learners.
- If you want, I can convert each acceptance criterion into curl-based test steps or pytest endpoints next.
