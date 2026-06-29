# Evidence: Build Question Storage And Validation

**ID:** o01-e02-build-question-storage-and-validation
**Task Ref:** `.devflow/tasks/o01/t02-build-question-storage-and-validation.md`
**Executed By:** Cursor
**Execution Date:** 2026-06-28
**Execution Time:** ~25 min
**Status:** completed

---

## 1. Summary

Implemented the Question Bank domain layer with a `Question` model, validation rules, SQLite schema migration v2, and a reusable `QuestionRepository` for create, read, update, delete, and search operations. Invalid payloads are rejected with explicit `ValidationError` messages, and omitted or blank difficulty values default to `Medium`.

---

## 2. Files Changed

| File                                                              | Change Type | Description                                  |
| ----------------------------------------------------------------- | ----------- | -------------------------------------------- |
| `backend/models.py`                                               | created     | Question dataclass and row mapping           |
| `backend/errors.py`                                               | created     | ValidationError with field metadata          |
| `backend/validation.py`                                           | created     | Question payload validation and defaults     |
| `backend/question_repository.py`                                  | created     | SQLite CRUD and search persistence layer     |
| `backend/database.py`                                             | modified    | Added migration v2 for `questions` table     |
| `tests/test_questions.py`                                         | created     | Validation and repository behavior tests     |
| `tests/test_bootstrap.py`                                         | modified    | Assert questions schema migration is applied |
| `.devflow/status.md`                                              | modified    | Updated runtime state after task completion  |
| `.devflow/tasks/o01/t02-build-question-storage-and-validation.md` | modified    | Marked task verified                         |

---

## 3. Behavior Added

* Questions can be created, listed, retrieved, updated, deleted, and searched in SQLite.
* Validation enforces required question text, options A-D, and correct answer values.
* Difficulty defaults to `Medium` when omitted or blank.
* Invalid payloads raise `ValidationError` with a field name for callers to handle later.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                         | Result | Notes                              |
| ----------------------------------------------------------------- | ------ | ---------------------------------- |
| Questions can be inserted, updated, deleted, listed, and searched | PASS   | Covered by repository tests        |
| Invalid question data is rejected per V1 rules                    | PASS   | Parametrized validation tests pass |
| Difficulty receives a default value when omitted                  | PASS   | Defaults to `Medium`               |

### Test Output

```
============================= test session starts =============================
collected 13 items

tests/test_bootstrap.py ...                                              [ 23%]
tests/test_questions.py ..........                                       [100%]

============================= 13 passed in 0.28s ==============================
```

---

## 5. Known Limitations

* HTTP API routes are intentionally not implemented in this task.
* Question IDs use SQLite autoincrement rather than `Date.now()` timestamps from the UI spec; API tasks can map as needed.
* Quiz cascade-delete behavior is out of scope until quiz features exist.

---

## 6. Next Suggested Task

**Next task:** `o01/t03-implement-question-bank-api`
**Context:** Expose `QuestionRepository` through Flask routes for list, search, create, update, and delete operations. Reuse `ValidationError` for HTTP 400 responses.
