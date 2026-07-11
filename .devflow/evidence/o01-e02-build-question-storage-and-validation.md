# Evidence: Build Question Storage And Validation

**ID:** o01-e02-build-question-storage-and-validation
**Task Ref:** `.devflow/tasks/o01/t02-build-question-storage-and-validation.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Execution Time:** 15:56-16:08 UTC+8, ~12 min
**Status:** completed

---

## 1. Summary

Implemented the V1 Question Bank domain and persistence layer in `backend/questions.py`, including normalized validation, default difficulty handling, SQLite-backed CRUD operations, and case-insensitive search by question text. Added automated tests covering repository behavior and invalid payload handling, and verified the full test suite successfully.

---

## 2. Files Changed

| File                      | Change Type | Description                                                                                                     |
| ------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------- |
| `backend/questions.py`    | created     | Added `Question` model, validation rules, validation error type, and SQLite repository methods for CRUD/search. |
| `tests/test_questions.py` | created     | Added tests for validation errors, default difficulty, CRUD, and search behavior.                               |
| `.devflow/status.md`      | modified    | Moved active runtime state to `o01/t02` during execution, then marked it verified and pointed to `o01/t03`.     |

---

## 3. Behavior Added

* Questions can now be created, read, updated, deleted, listed, and searched through a reusable SQLite repository layer.
* Invalid question payloads now fail with explicit backend validation errors instead of relying on frontend checks.
* Omitted difficulty values are normalized to the V1 default of `Medium`.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                                        | Result | Notes                                                                                   |
| ------------------------------------------------------------------------------------------------ | ------ | --------------------------------------------------------------------------------------- |
| Questions can be inserted, updated, deleted, listed, and searched through the persistence layer. | PASS   | Covered by repository CRUD/search tests against SQLite.                                 |
| Invalid question data is rejected according to the V1 validation rules.                          | PASS   | Covered by validation tests for missing/blank fields and invalid correct answer values. |
| Difficulty receives a default value when omitted.                                                | PASS   | Covered by direct validation test and repository create flow.                           |

### Test Output

```text
> py -m pytest
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 15 items

tests\test_bootstrap.py ...                                              [ 20%]
tests\test_questions.py ............                                     [100%]

============================= 15 passed in 0.18s ==============================
```

---

## 5. Known Limitations

* This task does not expose the repository through HTTP routes yet.
* Search currently filters only the question text, matching the V1 task and UI expectations.

---

## 6. Next Suggested Task

**Next task:** `o01/t03-implement-question-bank-api`
**Context:** The backend now has a reusable `QuestionRepository` and explicit validation errors, so the next task can focus on mapping HTTP requests and responses onto this layer without reworking persistence.
