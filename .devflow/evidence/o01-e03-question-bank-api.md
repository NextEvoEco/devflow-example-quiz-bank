# Evidence: Implement Question Bank API

**ID:** o01-e03-question-bank-api
**Task Ref:** `.devflow/tasks/o01/t03-implement-question-bank-api.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~30 min
**Status:** completed

---

## 1. Summary

Exposed the t02 storage layer through a lightweight REST API under `/api/questions`, using a Flask blueprint registered by the app factory. Endpoints cover list, search, get-one, create, update, and delete. Validation failures map to `400` with a per-field `fields` map, missing records map to `404`, and non-JSON bodies map to `400`. The repository is bound to the app via `app.config["QUESTION_REPOSITORY"]` so tests can inject an isolated database. Verified with 33 passing automated tests (11 new API tests) plus a live server run exercising every endpoint with `curl`.

---

## 2. Files Changed

| File                          | Change Type | Description                                                                                                                    |
| ----------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `backend/routes/__init__.py`  | created     | exports `questions_bp`                                                                                                         |
| `backend/routes/questions.py` | created     | `/api/questions` blueprint: list/search, get, create, update, delete; error mapping                                            |
| `backend/app.py`              | modified    | `create_app(db_path=None)` now builds a `QuestionRepository`, stores it on `app.config`, and registers the questions blueprint |
| `tests/test_questions_api.py` | created     | 11 API tests covering success and failure paths                                                                                |

---

## 3. Behavior Added

* `GET /api/questions` — list all questions; `?search=` filters by case-insensitive substring on question text.
* `GET /api/questions/<id>` — fetch one question, or `404` if absent.
* `POST /api/questions` — create; returns `201` with the created question, or `400` with a `fields` error map on validation failure.
* `PUT /api/questions/<id>` — update; `400` on validation failure, `404` if the id is absent.
* `DELETE /api/questions/<id>` — delete; `204` on success, `404` if absent.
* Non-JSON request bodies on create/update return `400` rather than a server error.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                       | Result | Notes                                                                                    |
| ------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------- |
| App exposes endpoints for list, search, create, update, delete                  | PASS   | Verified via `test_questions_api.py` and live curl against a running server              |
| Invalid inputs and missing-question cases return basic explicit error responses | PASS   | `400` with `fields` map for validation; `404` for missing ids; `400` for non-JSON bodies |
| Automated tests cover the main API success and failure paths                    | PASS   | 11 new API tests; full suite 33 passing                                                  |

### Test Output

```
$ python -m pytest tests/ -q
.................................                                        [100%]
33 passed in 0.51s

# Live server (py -m backend) curl checks:
POST /api/questions {"correct":"b", no difficulty} -> 201, correct normalized "B", difficulty "Medium"
GET  /api/questions                                -> 200, [ ... ]
GET  /api/questions?search=zzz                     -> 200, []
POST invalid (empty question, correct "Z")         -> 400 {"fields": {"question": ..., "correct": ...}}
GET  /api/questions/9999                            -> 404 {"error":"Question not found"}
DELETE /api/questions/1                             -> 204
```

---

## 5. Known Limitations

* No frontend rendering yet — the Question Bank list/editor UI is `o01/t04` and `o01/t05`.
* No pagination (matches `ui-spec.md`: "No built-in pagination — all filtered results are shown").
* No authentication/authorization — out of scope for V1.

---

## 6. Next Suggested Task

**Next task:** `o01/t04-build-question-bank-list-page`
**Context:** The API returns question objects keyed by `id, question, a, b, c, d, correct, difficulty` and serves the frontend shell from `frontend/` at `/`. The list page should fetch `GET /api/questions`, wire the search box to `?search=`, and render the question table + difficulty badge per `ui-spec.md`. Error responses use `{"error": ...}` and, for validation, `{"error": ..., "fields": {field: message}}` — useful when the editor page (t05) surfaces field errors.
