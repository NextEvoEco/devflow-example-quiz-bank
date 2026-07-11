# Evidence: Quiz CRUD API

**ID:** o02-e02-quiz-api
**Task Ref:** `.devflow/tasks/o02/t02-quiz-api.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Execution Time:** 17:08-17:18 UTC+8, ~10 min
**Status:** completed

---

## 1. Summary

Implemented the Quiz Builder backend API and repository layer, including quiz creation, listing, detail retrieval with ordered question objects, updates, deletes, and validation for minimum-question count, duplicate question IDs, and missing referenced questions. Verified the new quiz endpoints alongside the full existing Question Bank baseline.

---

## 2. Files Changed

| File                     | Change Type | Description                                                                                                    |
| ------------------------ | ----------- | -------------------------------------------------------------------------------------------------------------- |
| `backend/quizzes.py`     | created     | Added quiz validation, quiz repository, ordered question persistence, and detail/list query behavior.          |
| `backend/app.py`         | modified    | Added `/api/quizzes` CRUD routes, quiz payload parsing, quiz serialization, and quiz validation error mapping. |
| `tests/test_quiz_api.py` | created     | Added API tests for quiz create/list/detail/update/delete plus main validation failures.                       |
| `.devflow/status.md`     | modified    | Moved runtime state to `o02/t02`, then marked it verified and pointed to `o02/t03`.                            |

---

## 3. Behavior Added

* `GET /api/quizzes` now returns quiz summaries with question counts.
* `POST /api/quizzes` now creates quizzes from ordered question IDs and returns `201`.
* `GET /api/quizzes/<id>` now returns quiz details plus full ordered question objects for preview use.
* `PUT /api/quizzes/<id>` now updates quiz name and ordered question references.
* `DELETE /api/quizzes/<id>` now removes the quiz and its join-table references.
* Quiz saves now reject fewer than 3 questions, duplicate question IDs, and non-existent referenced question IDs with explicit `400` errors.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                       | Result | Notes                                      |
| ------------------------------------------------------------------------------- | ------ | ------------------------------------------ |
| `POST /api/quizzes` creates a quiz and returns 201                              | PASS   | Covered by API tests and live smoke check. |
| `POST /api/quizzes` with fewer than 3 questions returns 400                     | PASS   | Covered by API tests and live smoke check. |
| `POST /api/quizzes` with a non-existent question ID returns 400                 | PASS   | Covered by API tests.                      |
| `GET /api/quizzes` returns a list of quizzes                                    | PASS   | Covered by API tests and live smoke check. |
| `GET /api/quizzes/<id>` returns quiz details including ordered question objects | PASS   | Covered by API tests and live smoke check. |
| `PUT /api/quizzes/<id>` updates name and/or question list                       | PASS   | Covered by API tests and live smoke check. |
| `DELETE /api/quizzes/<id>` removes the quiz and its question references         | PASS   | Covered by API tests and live smoke check. |
| All existing Question Bank API tests continue to pass                           | PASS   | Full test suite remained green.            |

### Test Output

```text
> py -m pytest tests -v
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 38 items
...
tests/test_quiz_api.py::test_create_quiz_returns_201 PASSED
tests/test_quiz_api.py::test_create_quiz_rejects_fewer_than_three_questions PASSED
tests/test_quiz_api.py::test_create_quiz_rejects_missing_question_ids PASSED
tests/test_quiz_api.py::test_create_quiz_rejects_duplicate_question_ids PASSED
tests/test_quiz_api.py::test_list_quizzes_returns_quiz_summaries PASSED
tests/test_quiz_api.py::test_get_quiz_returns_ordered_question_details PASSED
tests/test_quiz_api.py::test_update_quiz_replaces_name_and_question_order PASSED
tests/test_quiz_api.py::test_delete_quiz_removes_quiz_and_references PASSED
...
============================= 38 passed in 0.79s ==============================

> live quiz API smoke
POST invalid /api/quizzes -> 400 with minimum-question error
POST /api/quizzes -> 201
GET /api/quizzes -> summary list returned
GET /api/quizzes/<id> -> ordered question details returned
PUT /api/quizzes/<id> -> reordered questionIds returned
DELETE /api/quizzes/<id> -> 200
```

---

## 5. Known Limitations

* This task adds only the backend API; no Quiz Builder frontend pages consume these endpoints yet.
* Quiz payloads currently include only the fields required by the confirmed V1 scope: name and ordered question references.

---

## 6. Next Suggested Task

**Next task:** `o02/t03-quiz-list-page`
**Context:** The backend now exposes a stable `/api/quizzes` contract, so the next step can build the Quiz list UI on top of live quiz summaries and delete actions.
