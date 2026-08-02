# Submission instructions

Working branch: `mid-course-project`.

What to submit:
- A public repository URL with the `mid-course-project` branch containing your changes.
- The `docs/midcourse/` folder containing the required documentation files.

How to run the app and tests:
```bash
# start the backend
uvicorn app.main:app --reload --port 8000

# run tests (in a virtualenv)
pip install -r requirements.txt
pytest -q
```
