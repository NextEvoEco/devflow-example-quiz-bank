# Evidence: Quiz CRUD API

**ID:** o02-e02-quiz-api
**Task Ref:** `.devflow/tasks/o02/t02-quiz-api.md`
**Executed By:** Cursor
**Execution Date:** 2026-07-09
**Execution Time:** ~10:26 UTC+8
**Status:** completed

---

## 1. Summary

Implemented the Quiz Builder backend API with `QuizRepository`, quiz payload validation, and Flask routes under `/api/quizzes`. The API supports quiz list, create, retrieve, update, and delete flows with ordered question references and full question details on single-quiz responses.

---

## 2. Files Changed

| File                                 | Change Type | Description                                       |
| ------------------------------------ | ----------- | ------------------------------------------------- |
| `backend/quiz_validation.py`         | created     | Quiz payload validation rules                     |
| `backend/quiz_repository.py`         | created     | Quiz persistence and question ordering            |
| `backend/routes/quizzes.py`          | created     | Quiz CRUD HTTP endpoints                          |
| `backend/app.py`                     | modified    | Registered quizzes blueprint                      |
| `tests/test_quizzes_api.py`          | created     | Quiz API integration tests                        |
| `tests/test_release_verification.py` | modified    | Removed `/api/quizzes` from V1 out-of-scope check |

---

## 3. Behavior Added

* `GET /api/quizzes` — list quizzes with `id`, `name`, `questionCount`
* `POST /api/quizzes` — create quiz from `name` + `questionIds` (min 3, no duplicates, IDs must exist)
* `GET /api/quizzes/<id>` — quiz with ordered full question objects
* `PUT /api/quizzes/<id>` — update name and/or question list
* `DELETE /api/quizzes/<id>` — delete quiz and join rows (cascade)

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                 | Result | Notes              |
| ----------------------------------------- | ------ | ------------------ |
| POST creates quiz (201)                   | PASS   | Full flow test     |
| POST with <3 questions returns 400        | PASS   | Validation test    |
| POST with missing question ID returns 400 | PASS   | Existence check    |
| GET list returns quizzes                  | PASS   | List endpoint test |
| GET by id returns ordered questions       | PASS   | Full flow test     |
| PUT updates name/questions                | PASS   | Full flow test     |
| DELETE removes quiz                       | PASS   | Full flow test     |
| Question Bank tests still pass            | PASS   | 44/44 total        |

### Test Output

```
44 passed in 0.72s
```

---

## 5. Known Limitations

* No frontend Quiz Builder UI yet.
* Quiz payload has no `description` field (schema t01 only has `name`).

---

## 6. Next Suggested Task

**Next task:** `o02/t03-quiz-list-page`
**Context:** Build the Quiz Builder list page frontend.
