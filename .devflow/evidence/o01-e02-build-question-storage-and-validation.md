# Evidence: Build Question Storage And Validation

**ID:** o01-e02-build-question-storage-and-validation
**Task Ref:** `.devflow/tasks/o01/t02-build-question-storage-and-validation.md`
**Executed By:** Cursor
**Execution Date:** 2026-07-08
**Execution Time:** ~23:22-23:25 UTC+8
**Status:** completed

---

## 1. Summary

Implemented the Question Bank persistence and validation layer with a SQLite `questions` table (migration v1), reusable validation rules, and a `QuestionRepository` supporting create, read, update, delete, list, and search. Invalid payloads are rejected with explicit field-level errors, and omitted difficulty defaults to `Medium`.

---

## 2. Files Changed

| File                                | Change Type | Description                                       |
| ----------------------------------- | ----------- | ------------------------------------------------- |
| `backend/validation.py`             | created     | Question payload validation and `ValidationError` |
| `backend/question_repository.py`    | created     | SQLite-backed CRUD and search repository          |
| `backend/db.py`                     | modified    | Added migration v1 for `questions` table          |
| `tests/test_question_repository.py` | created     | Validation and repository tests                   |
| `.devflow/status.md`                | modified    | Runtime state for o01/t02                         |

---

## 3. Behavior Added

* Questions are stored in SQLite with fields matching the UI spec (`question`, `a`–`d`, `correct`, `difficulty`).
* `QuestionRepository` supports insert, list, search, update, and delete.
* Search filters by case-insensitive substring match on question text.
* Validation enforces required question text, options A–D, and correct answer (`A`–`D`).
* Omitted difficulty is defaulted to `Medium`.
* Missing records raise `QuestionNotFoundError`.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                         | Result | Notes                                  |
| ----------------------------------------------------------------- | ------ | -------------------------------------- |
| Questions can be inserted, updated, deleted, listed, and searched | PASS   | Covered by repository integration test |
| Invalid question data is rejected with validation rules           | PASS   | Covered by validation unit tests       |
| Difficulty receives a default value when omitted                  | PASS   | Defaults to `Medium`                   |

### Test Output

```
tests/test_bootstrap.py::test_health_endpoint PASSED
tests/test_bootstrap.py::test_index_page_is_served PASSED
tests/test_bootstrap.py::test_database_initializes_on_startup PASSED
tests/test_question_repository.py::test_validate_question_payload_defaults_difficulty PASSED
tests/test_question_repository.py::test_validate_question_payload_rejects_missing_option PASSED
tests/test_question_repository.py::test_validate_question_payload_rejects_invalid_correct_answer PASSED
tests/test_question_repository.py::test_create_list_search_update_delete PASSED
tests/test_question_repository.py::test_delete_missing_question_raises PASSED

8 passed in 0.27s
```

---

## 5. Known Limitations

* No HTTP routes were added; API exposure is deferred to `o01/t03`.
* Question IDs use SQLite autoincrement rather than `Date.now()` from the UI spec prototype.

---

## 6. Next Suggested Task

**Next task:** `o01/t03-implement-question-bank-api`
**Context:** Expose `QuestionRepository` through `/api/questions` endpoints and map validation errors to HTTP responses.
