# Evidence: Build Question Storage And Validation

**ID:** o01-e02-question-storage-and-validation
**Task Ref:** `.devflow/tasks/o01/t02-build-question-storage-and-validation.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~30 min
**Status:** completed

---

## 1. Summary

Built the Question Bank domain layer on top of the t01 bootstrap: a `questions` SQLite table (added via a versioned migration using `PRAGMA user_version`), a `Question` entity, reusable validation rules, and a `QuestionRepository` providing create/read/update/delete/search. Validation and persistence are enforced at the storage layer (not the frontend), so later API and UI tasks can rely on a single source of truth. Verified with 22 passing automated tests covering CRUD, case-insensitive search, required-field enforcement, correct-answer normalization, and difficulty defaulting.

---

## 2. Files Changed

| File                                | Change Type | Description                                                                                                                                                                         |
| ----------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `backend/database.py`               | modified    | Added `questions` table schema + versioned `_migrate()` (PRAGMA user_version); `get_connection`/`init_db` now accept an optional `db_path` for test isolation; enabled foreign keys |
| `backend/models.py`                 | created     | `Question` dataclass (UI-spec field shape) + `question_from_row()` row mapper                                                                                                       |
| `backend/validation.py`             | created     | `validate_question()`, `ValidationError` (per-field error map), difficulty/answer constants and `DEFAULT_DIFFICULTY`                                                                |
| `backend/question_repository.py`    | created     | `QuestionRepository` with create/get/list(search)/update/delete over SQLite                                                                                                         |
| `tests/test_question_repository.py` | created     | 20 tests for CRUD, search, and validation behavior                                                                                                                                  |

---

## 3. Behavior Added

* Questions can be inserted, fetched, listed, updated, deleted, and searched through `QuestionRepository`.
* Search performs a case-insensitive substring match on question text (matches the `filteredQuestions` rule in `ui-spec.md`).
* Invalid payloads raise `ValidationError` carrying a per-field error map; required fields (question, a-d, correct) are enforced and text is trimmed.
* `correct` is normalized to uppercase and must be one of A/B/C/D; `difficulty` is normalized (e.g. `hard` → `Hard`) and must be Easy/Medium/Hard.
* Omitted or blank `difficulty` defaults to `Medium`.
* The database schema is applied through a versioned migration so later tasks can add tables without restructuring.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                                       | Result | Notes                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Questions can be inserted, updated, deleted, listed, and searched through the persistence layer | PASS   | Covered by `test_create_and_get`, `test_list_returns_all_ordered`, `test_update_changes_fields`, `test_delete_removes_question`, `test_search_is_case_insensitive_substring` |
| Invalid question data is rejected according to the V1 validation rules                          | PASS   | Missing required text fields, missing/invalid `correct`, and invalid `difficulty` all raise `ValidationError`                                                                |
| Difficulty receives a default value when omitted                                                | PASS   | `test_omitted_difficulty_gets_default` and `test_empty_difficulty_gets_default` assert `Medium`                                                                              |

### Test Output

```
$ python -m pytest tests/ -v
collected 22 items
tests/test_bootstrap.py ..                                        [  9%]
tests/test_question_repository.py ....................            [100%]
============================== 22 passed in 0.38s ==============================
```

---

## 5. Known Limitations

* No HTTP routing yet — exposing `/api/questions` is deferred to `o01/t03` per task boundary.
* No frontend rendering — deferred to `o01/t04`.
* `id` is assigned by SQLite `AUTOINCREMENT`; the `ui-spec.md` note about `Date.now()` is a frontend-era detail and is intentionally not reproduced in the backend storage layer.
* Difficulty default is `Medium` (chosen as a sensible middle value; `ui-spec.md` does not mandate a specific default).

---

## 6. Next Suggested Task

**Next task:** `o01/t03-implement-question-bank-api`
**Context:** `QuestionRepository` returns JSON-ready dicts keyed by `id, question, a, b, c, d, correct, difficulty`, so the API layer can serialize results directly. Validation failures surface as `ValidationError` with an `errors` dict — the API task should map these to a 400 response body. Repository/DB accept an optional `db_path`, but `create_app()` uses the default `data/quiz_bank.db`; construct `QuestionRepository()` with no arguments in the app.
