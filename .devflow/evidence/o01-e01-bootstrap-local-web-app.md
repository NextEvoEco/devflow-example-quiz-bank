# Evidence: Bootstrap Local Web App Foundation

**ID:** o01-e01-bootstrap-local-web-app
**Task Ref:** `.devflow/tasks/o01/t01-bootstrap-local-web-app.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~30 min
**Status:** completed

---

## 1. Summary

The `backend/`, `frontend/`, and `tests/` directories contained no tracked source files before this task (only orphaned `__pycache__` bytecode from a prior, uncommitted implementation). This task built the minimal runnable Quiz Bank foundation from scratch: a Flask app factory that serves a static frontend shell and bootstraps a SQLite database file on first start, plus a bootstrap test and updated run instructions. The app was started as a real local server and hit with `curl` to confirm it serves correctly; the deleted stale `__pycache__`/`.pytest_cache` artifacts and the empty `backend/routes/` directory left over from the prior implementation were removed as part of establishing a clean starting structure.

---

## 2. Files Changed

| File                                                                              | Change Type | Description                                                             |
| --------------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------- |
| `backend/__init__.py`                                                             | created     | exposes `create_app` for the package                                    |
| `backend/config.py`                                                               | created     | base dir, data dir, frontend dir, and database path constants           |
| `backend/database.py`                                                             | created     | `get_connection()` and `init_db()` bootstrap for the SQLite file        |
| `backend/app.py`                                                                  | created     | Flask app factory, serves frontend static assets and `/` shell page     |
| `backend/__main__.py`                                                             | created     | entrypoint so the app can run via `py -m backend`                       |
| `frontend/index.html`                                                             | created     | minimal shell page                                                      |
| `frontend/css/style.css`                                                          | created     | minimal base styling                                                    |
| `frontend/js/app.js`                                                              | created     | placeholder frontend script                                             |
| `tests/test_bootstrap.py`                                                         | created     | verifies the shell page is served and the DB file is initialized        |
| `requirements.txt`                                                                | created     | `flask>=3.0,<4.0`, `pytest>=8.0,<9.0`                                   |
| `data/.gitkeep`                                                                   | created     | keeps the runtime data directory present in the repo                    |
| `.gitignore`                                                                      | modified    | ignore `data/*.db` runtime database files                               |
| `README.md`                                                                       | modified    | added "Running The Application" section (install, start, test commands) |
| `backend/__pycache__/`, `backend/routes/`, `tests/__pycache__/`, `.pytest_cache/` | deleted     | stale artifacts from a prior, never-committed implementation            |

---

## 3. Behavior Added

* The app can be started locally with `py -m backend` and serves a minimal HTML shell page at `/`.
* Static frontend assets (`css/`, `js/`) are served by Flask from `frontend/`.
* The SQLite database file (`data/quiz_bank.db`) is created automatically on first start with no manual setup.
* Automated tests can be run with `py -m pytest`.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                         | Result | Notes                                                                                                                         |
| --------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| Repository has a stable local app structure for backend, frontend, and tests      | PASS   | `backend/`, `frontend/`, `tests/` created with the entrypoint/config/database/app split                                       |
| Application can be started by a Python command and serve at least a minimal page  | PASS   | `py -m backend` started a real server; `curl http://127.0.0.1:5000/` returned HTTP 200 with "Quiz Bank" shell content         |
| SQLite initialization runs on first start without requiring manual database setup | PASS   | `data/quiz_bank.db` was created automatically on first `create_app()` call, confirmed both via `pytest` and a live server run |

### Test Output

```
$ python -m pytest tests/ -v
tests/test_bootstrap.py::test_app_serves_minimal_shell_page PASSED       [ 50%]
tests/test_bootstrap.py::test_database_is_initialized_on_first_start PASSED [100%]
============================== 2 passed in 0.17s ==============================

$ python -m backend  (manual run, then curl in a separate shell)
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:5000/       -> HTTP 200
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:5000/css/style.css -> HTTP 200
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:5000/js/app.js     -> HTTP 200
data/quiz_bank.db created after first request
```

---

## 5. Known Limitations

* No question schema, CRUD, or validation yet — intentionally deferred to `o01/t02` per task boundary.
* No HTTP API routes yet — deferred to `o01/t03`.
* The frontend shell is a static placeholder page, not the full sidebar/top-bar layout from `ui-spec.md` — that begins in `o01/t04`.

---

## 6. Next Suggested Task

**Next task:** `o01/t02-build-question-storage-and-validation`
**Context:** The bootstrap intentionally left `init_db()` schema-less (it only ensures the SQLite file exists) so `o01/t02` can define the `questions` table, migrations, and validation rules without reconciling a premature schema. Note the memory entry recorded on 2026-07-07 — context files and task "Status: verified" markers in this repo do not reliably reflect what code actually exists on disk; verify against `backend/`, `frontend/`, `tests/` directly before assuming later tasks are already implemented.
