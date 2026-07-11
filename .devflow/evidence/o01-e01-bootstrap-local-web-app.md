# Evidence: Bootstrap Local Web App Foundation

**ID:** o01-e01-bootstrap-local-web-app
**Task Ref:** `.devflow/tasks/o01/t01-bootstrap-local-web-app.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Execution Time:** 15:30-15:55 UTC+8, ~25 min
**Status:** completed

---

## 1. Summary

Built the initial runnable V1 application foundation for Quiz Bank with a Flask app factory, `py -m backend` startup entrypoint, automatic SQLite initialization, a minimal static frontend shell, and bootstrap tests. The repository state and context artifacts were also corrected to match the live workspace before verification.

---

## 2. Files Changed

| File                                 | Change Type | Description                                                                    |
| ------------------------------------ | ----------- | ------------------------------------------------------------------------------ |
| `backend/__init__.py`                | created     | Added backend package marker.                                                  |
| `backend/__main__.py`                | created     | Added local startup entrypoint for `py -m backend`.                            |
| `backend/app.py`                     | created     | Added Flask app factory, index route, and healthcheck route.                   |
| `backend/config.py`                  | created     | Added shared filesystem path configuration.                                    |
| `backend/db.py`                      | created     | Added first-run SQLite initialization and baseline schema.                     |
| `frontend/index.html`                | created     | Added minimal Quiz Bank shell page.                                            |
| `frontend/styles.css`                | created     | Added bootstrap shell styling.                                                 |
| `frontend/app.js`                    | created     | Added startup healthcheck request for UI confirmation.                         |
| `tests/conftest.py`                  | created     | Added pytest app and client fixtures.                                          |
| `tests/test_bootstrap.py`            | created     | Added startup, health, and database bootstrap tests.                           |
| `requirements.txt`                   | created     | Added Flask and pytest dependencies.                                           |
| `README.md`                          | modified    | Added accurate structure and local startup instructions.                       |
| `.devflow/status.md`                 | modified    | Set current runtime state for task execution and verification.                 |
| `.devflow/memory.md`                 | modified    | Recorded the artifact/code mismatch discovered during execution.               |
| `.devflow/context/repo-structure.md` | modified    | Realigned repository structure context to the actual bootstrap implementation. |
| `.devflow/context/architecture.md`   | modified    | Realigned architecture context to the actual bootstrap implementation.         |

---

## 3. Behavior Added

* The project can now be started locally with `py -m backend`.
* The app automatically creates `data/quiz_bank.db` and the `questions` table on first run.
* The browser can load a minimal Quiz Bank shell page from Flask.
* Bootstrap verification can be run with `py -m pytest`.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                                          | Result | Notes                                                                             |
| -------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------- |
| The repository has a stable local app structure for backend, frontend, and tests.                  | PASS   | Added `backend/`, `frontend/`, `tests/`, and dependency bootstrap files.          |
| The application can be started by a Python command and serve at least a minimal page successfully. | PASS   | Verified with `py -m backend` plus live checks against `/` and `/health`.         |
| SQLite initialization runs on first start without requiring manual database setup.                 | PASS   | Startup initializes `data/quiz_bank.db`; tests also verify the `questions` table. |

### Test Output

```text
> py -m pip install -r requirements.txt
Requirement already satisfied: Flask<4.0,>=3.0
Requirement already satisfied: pytest<9.0,>=8.0

> py -m pytest
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 3 items
tests\test_bootstrap.py ...                                              [100%]
============================== 3 passed in 0.08s ==============================

> live startup check
GET / -> 200
GET /health -> 200
health body -> {"database_path":"D:\\Develop\\workspace\\devflow-example-quiz-bank\\data\\quiz_bank.db","status":"ok"}
```

---

## 5. Known Limitations

* Question Bank CRUD routes and UI are intentionally not implemented in this task.
* The current backend only serves `/` and `/health`; later V1 tasks will add Question Bank APIs.

---

## 6. Next Suggested Task

**Next task:** `o01/t02-build-question-storage-and-validation`
**Context:** The repository now has a stable Flask + SQLite foundation. The next step can build real question persistence and validation without restructuring the app layout.
