# Evidence: Quiz CRUD API

**ID:** o02-e02-quiz-api
**Task Ref:** `.devflow/tasks/o02/t02-quiz-api.md`
**Executed By:** Cursor
**Execution Date:** 2026-06-28
**Execution Time:** ~30 min
**Status:** completed

---

## 1. Summary

Implemented the Quiz Builder backend API with `QuizRepository`, validation rules, and Flask routes for list, create, read, update, and delete. Quizzes store ordered question references only, enforce a minimum of 3 questions, validate question IDs, and return full question objects on detail responses for preview support.

---

## 2. Files Changed

| File | Change Type | Description |
| --- | --- | --- |
| `backend/models.py` | modified | Added `QuizSummary` and `QuizDetail` models |
| `backend/quiz_validation.py` | created | Quiz payload validation rules |
| `backend/quiz_repository.py` | created | Quiz persistence and question ordering |
| `backend/routes/quizzes.py` | created | `/api/quizzes` HTTP endpoints |
| `backend/app.py` | modified | Registered quiz repository and blueprint |
| `tests/test_quizzes_api.py` | created | Quiz API success and failure tests |
| `tests/test_v1_release.py` | modified | Removed `/api/quizzes` from V1 out-of-scope route check |
| `.devflow/status.md` | modified | Updated runtime state after task completion |
| `.devflow/tasks/o02/t02-quiz-api.md` | modified | Marked task verified |

---

## 3. Behavior Added

* `GET /api/quizzes` lists quizzes with `questionCount`
* `POST /api/quizzes` creates a quiz from `name` and ordered `questionIds`
* `GET /api/quizzes/<id>` returns quiz details with full ordered question objects
* `PUT /api/quizzes/<id>` updates quiz name and/or question list
* `DELETE /api/quizzes/<id>` deletes quiz and join-table references
* Validation rejects fewer than 3 questions, duplicate IDs, and missing question IDs

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion | Result | Notes |
| --- | --- | --- |
| `POST /api/quizzes` creates quiz and returns 201 | PASS | |
| Fewer than 3 questions returns 400 | PASS | create and update |
| Non-existent question ID returns 400 | PASS | |
| `GET /api/quizzes` returns list | PASS | |
| `GET /api/quizzes/<id>` returns ordered question objects | PASS | |
| `PUT /api/quizzes/<id>` updates quiz | PASS | |
| `DELETE /api/quizzes/<id>` removes quiz references | PASS | questions remain |
| Existing Question Bank tests still pass | PASS | 50 tests total |

### Test Output

```
============================= 50 passed in 1.27s ==============================
```

---

## 5. Known Limitations

* No frontend Quiz Builder UI yet.
* Quiz payload uses `questionIds` only; no alternate key alias.
* Name-only update without `questionIds` is supported, but not separately tested.

---

## 6. Next Suggested Task

**Next task:** `o02/t03-quiz-list-page`
**Context:** Build the Quiz list frontend and wire it to `/api/quizzes`.
