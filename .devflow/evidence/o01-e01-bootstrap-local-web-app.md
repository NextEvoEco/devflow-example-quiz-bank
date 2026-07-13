# Evidence: Bootstrap Local Web App Foundation

**ID:** o01-e01-bootstrap-local-web-app
**Task Ref:** `.devflow/tasks/o01/t01-bootstrap-local-web-app.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-11
**Execution Time:** ~17:30-17:50 UTC+8, ~20 min
**Status:** completed

---

## 1. Summary

Created the Quiz Bank local-app foundation: Flask entrypoint (`py -m backend`), SQLite auto-init with versioned migrations (v1 `questions` table), Vue 3 + TypeScript Vite frontend shell built to `frontend/dist/` and served by Flask, plus bootstrap pytest coverage. Verified health API, HTML shell, and automatic DB creation against the running server.

---

## 2. Files Changed

| File                          | Change Type | Description                          |
| ----------------------------- | ----------- | ------------------------------------ |
| `backend/__init__.py`         | created     | Package marker                       |
| `backend/__main__.py`         | created     | `py -m backend` entrypoint           |
| `backend/app.py`              | created     | Flask factory, health + static serve |
| `backend/config.py`           | created     | Paths, host, port                    |
| `backend/database.py`         | created     | SQLite bootstrap + migrations        |
| `frontend/*`                  | created     | Vite Vue 3 + TS project shell        |
| `tests/conftest.py`           | created     | Shared fixtures                      |
| `tests/test_bootstrap.py`     | created     | Startup/DB smoke tests               |
| `requirements.txt`            | created     | Flask + pytest                       |
| `.gitignore`                  | modified    | data/, node_modules/, dist/          |
| `README.md`                   | modified    | Run/test instructions                |
| `docs/getting-started-app.md` | created     | App startup guide                    |

---

## 3. Behavior Added

* App starts with `py -m backend` on http://127.0.0.1:5000
* SQLite `data/quiz_bank.db` created and migrated on first start
* Built Vue shell is served from `frontend/dist/`
* `/api/health` returns `{"status":"ok"}`

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                               | Result | Notes                              |
| --------------------------------------- | ------ | ---------------------------------- |
| Stable backend/frontend/tests structure | PASS   | Created as planned                 |
| Python command serves minimal page      | PASS   | GET / returns Vue shell HTML       |
| SQLite init on first start              | PASS   | `data/quiz_bank.db` with schema v1 |

### Test Output

```
py -m pytest tests -v
3 passed

npm run build
✓ built successfully

HTTP smoke (running app):
GET /api/health → {"status":"ok"}
GET / → 200, contains #app
DB tables: schema_migrations, questions; version 1
```

---

## 5. Known Limitations

* Question Bank CRUD UI/API not yet implemented (later o01 tasks)
* Frontend is a layout shell only

---

## 6. Next Suggested Task

**Next task:** `o01/t02-build-question-storage-and-validation`
**Context:** Reuse `backend/database.py` migration pattern and `create_app` factory; add models/repository/validation without HTTP routes yet.
