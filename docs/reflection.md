# Reflection (250–500 words)

During this task I used AI-assisted edits to implement server-side filtering and a modal-only comments UI. Overall I aimed to keep the implementation simple, testable, and easy to run locally.

Which AI tools I used and for what
- The assistant (AI) was used interactively to generate code changes across the frontend and backend. It drafted Pydantic models, FastAPI route handlers, and frontend JavaScript to call the APIs. It also produced pytest tests and documentation drafts.

One moment AI helped
- The AI scaffolded the initial comments subresource and suggested validation via Pydantic. That save time and provided consistent request/response models I could wire into the routes and frontend quickly.

One moment AI slowed me down
- Early on the AI suggested showing comments in both Create and Edit modals, and displaying per-card comment counts. That didn't match the product constraint (no orphan comments); I spent time removing those parts and re-wiring the modal behavior. The back-and-forth cost time but produced a clearer design.

Where my review changed the result
- I rejected an initial client-only filtering suggestion in favor of server-side support for `q`, status, priority, and assignee. I also decided comments must be modal-only; these product decisions simplified edge cases and made the UX consistent.

Takeaways
- The AI is extremely useful for repetitive scaffolding (models, routes, tests). Always review suggestions for product constraints. Small projects benefit from the AI doing heavy lifting, but the product owner needs to catch the assumptions early (e.g., where to show comments).

