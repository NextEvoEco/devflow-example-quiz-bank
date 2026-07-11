# Evidence: Bootstrap Local Web App Foundation

**ID:** o01-e01-bootstrap-local-web-app
**Task Ref:** `.devflow/tasks/o01/t01-bootstrap-local-web-app.md`
**Executed By:** Cursor
**Execution Date:** 2026-07-08
**Execution Time:** ~22:49-23:00 UTC+8
**Status:** completed

---

## 1. Summary

Bootstrapped the Quiz Bank local web application foundation with a Flask backend, static frontend shell, SQLite initialization on first run, and basic automated tests. The application can be started with `py -m backend` and serves a minimal shell page at `http://127.0.0.1:5000/`.

At execution time the repository had DevFlow task/context artifacts but no application source under `backend/`, `frontend/`, or `tests/`. This task recreated the missing foundation so later o01 tasks have a stable layout.

---

## 2. Files Changed

| File                      | Change Type | Description                                             |
| ------------------------- | ----------- | ------------------------------------------------------- |
| `backend/__init__.py`     | created     | Backend package marker                                  |
| `backend/__main__.py`     | created     | Local server entrypoint (`py -m backend`)               |
| `backend/app.py`          | created     | Flask app factory, static file serving, health endpoint |
| `backend/config.py`       | created     | Paths, host, and port configuration                     |
| `backend/db.py`           | created     | SQLite bootstrap with `schema_migrations` table         |
| `frontend/index.html`     | created     | Minimal application shell page                          |
| `frontend/css/styles.css` | created     | Base layout styles for sidebar and content shell        |
| `frontend/js/app.js`      | created     | Minimal frontend bootstrap script                       |
| `tests/test_bootstrap.py` | created     | Bootstrap verification tests                            |
| `requirements.txt`        | created     | Flask and pytest dependencies                           |
| `docs/app-startup.md`     | created     | Install and startup instructions                        |
| `README.md`               | modified    | Added quick-start section                               |
| `.gitignore`              | modified    | Ignore generated `data/` directory                      |
| `.devflow/status.md`      | modified    | Runtime state for o01/t01 execution                     |

---

## 3. Behavior Added

* The repository now has a stable `backend/`, `frontend/`, and `tests/` layout.
* Running `py -m backend` starts a local Flask server on port 5000.
* The root URL serves a minimal Quiz Bank shell page with sidebar and top bar layout.
* SQLite is initialized automatically on first start at `data/quiz_bank.db`.
* A `/api/health` endpoint returns `{"status": "ok"}` for basic verification.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                       | Result | Notes                                                             |
| --------------------------------------------------------------- | ------ | ----------------------------------------------------------------- |
| Stable local app structure for backend, frontend, and tests     | PASS   | Directories and entrypoints created                               |
| Application starts via Python command and serves a minimal page | PASS   | Flask test client returned 200 with shell content                 |
| SQLite initialization runs on first start without manual setup  | PASS   | `data/quiz_bank.db` and `schema_migrations` created automatically |

### Test Output

```
tests/test_bootstrap.py::test_health_endpoint PASSED
tests/test_bootstrap.py::test_index_page_is_served PASSED
tests/test_bootstrap.py::test_database_initializes_on_startup PASSED

============================== 3 passed in 0.22s ==============================

Smoke check:
status 200
shell True
health {'status': 'ok'}
db_exists True
```

---

## 5. Known Limitations

* Question Bank business behavior is intentionally not implemented in this task.
* Navigation items in the shell are disabled placeholders.
* Full question schema and CRUD persistence are deferred to `o01/t02`.
* `.devflow/context/*` previously described a fully implemented V1–V3 app; those files are ahead of the live code after this bootstrap and should be treated as target/history, not current implementation truth.

---

## 6. Next Suggested Task

**Next task:** `o01/t02-build-question-storage-and-validation`
**Context:** Extend `backend/db.py` with the questions schema and add repository/validation code under `backend/` for later API and UI tasks.
