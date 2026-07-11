# Evidence: Quiz Database Schema

**ID:** o02-e01-quiz-db-schema
**Task Ref:** `.devflow/tasks/o02/t01-quiz-db-schema.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Execution Time:** 17:00-17:07 UTC+8, ~7 min
**Status:** completed

---

## 1. Summary

Extended the SQLite bootstrap logic to a lightweight versioned migration runner and added the V2 quiz schema tables `quizzes` and `quiz_questions`. Verified that startup applies both schema versions automatically and that existing Question Bank data remains intact after migration.

---

## 2. Files Changed

| File                        | Change Type | Description                                                                                                                           |
| --------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `backend/db.py`             | modified    | Replaced the single-schema bootstrap with a versioned migration runner and added schema version 2 for `quizzes` and `quiz_questions`. |
| `tests/test_quiz_schema.py` | created     | Added tests for new quiz table creation and migration safety for existing `questions` data.                                           |
| `.devflow/status.md`        | modified    | Moved runtime state to `o02/t01`, then marked it verified and pointed to `o02/t02`.                                                   |

---

## 3. Behavior Added

* App startup now records applied schema versions in `schema_migrations`.
* SQLite initialization now creates `quizzes` with `id`, `name`, and `created_at`.
* SQLite initialization now creates `quiz_questions` with `quiz_id`, `question_id`, and `position`, including foreign keys.
* Existing `questions` data survives migration to the new quiz schema baseline.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                       | Result | Notes                                                            |
| ------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------- |
| App starts without errors after schema change                                   | PASS   | Verified through full pytest run and direct startup smoke check. |
| `quizzes` table exists with `id`, `name`, `created_at` columns                  | PASS   | Verified in dedicated schema test and startup smoke check.       |
| `quiz_questions` table exists with `quiz_id`, `question_id`, `position` columns | PASS   | Verified in dedicated schema test and startup smoke check.       |
| Existing `questions` table and data are unaffected                              | PASS   | Verified in migration-preservation test.                         |

### Test Output

```text
> py -m pytest tests -v
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 30 items
...
tests/test_quiz_schema.py::test_quiz_schema_tables_are_created PASSED
tests/test_quiz_schema.py::test_quiz_schema_migration_preserves_existing_question_data PASSED
...
============================= 30 passed in 0.51s ==============================

> startup schema smoke
tables -> questions, quiz_questions, quizzes, schema_migrations
quizzes columns -> id, name, created_at
quiz_questions columns -> quiz_id, question_id, position
```

---

## 5. Known Limitations

* This task adds only the schema foundation; no quiz repository or API behavior exists yet.
* The migration runner is intentionally lightweight and local-app scoped rather than a full migration framework.

---

## 6. Next Suggested Task

**Next task:** `o02/t02-quiz-api`
**Context:** The quiz tables are now present and startup-safe, so the next step can implement quiz CRUD and ordered question reference behavior on top of them.
