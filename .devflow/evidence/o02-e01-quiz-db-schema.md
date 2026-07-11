# Evidence: Quiz Database Schema

**ID:** o02-e01-quiz-db-schema
**Task Ref:** `.devflow/tasks/o02/t01-quiz-db-schema.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~20 min
**Status:** completed

---

## 1. Summary

Extended the SQLite schema to schema version 2 to support Quiz Builder, following
the existing `PRAGMA user_version` migration pattern. Added a `quizzes` table
(`id`, `name`, `created_at`) and a `quiz_questions` ordered join table
(`quiz_id`, `question_id`, `position`) that stores only references — no question
content. Both foreign keys are defined; `ON DELETE CASCADE` keeps join rows
consistent when a quiz or a referenced question is removed. The v1 `questions`
table and its data are untouched. Verified with 60 passing tests (8 new) and a
fresh-start inspection confirming `user_version = 2` and the exact columns.

---

## 2. Files Changed

| File                        | Change Type | Description                                                                                                            |
| --------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| `backend/database.py`       | modified    | `SCHEMA_VERSION` → 2; added `quizzes` + `quiz_questions` table DDL and a `version < 2` migration step                  |
| `tests/test_quiz_schema.py` | created     | 8 tests: schema version, table columns, FKs, integer position, questions-unaffected, idempotent re-run, cascade delete |

---

## 3. Behavior Added

* On startup, a database at schema v1 (or a fresh database) migrates to v2 by
  creating `quizzes` and `quiz_questions`; a database already at v2 is left as-is.
* `quiz_questions.position` is an integer preserving manual question ordering.
* Deleting a quiz cascades to remove its `quiz_questions` rows; deleting a
  referenced question likewise removes its join rows (so the V1 question-delete
  flow keeps working once quizzes exist).

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                               | Result | Notes                                                                                    |
| ----------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------- |
| App starts without errors after schema change                           | PASS   | `create_app()` on a fresh DB migrated to v2; no errors                                   |
| `quizzes` table exists with `id`, `name`, `created_at`                  | PASS   | `test_quizzes_table_columns`; confirmed by manual `PRAGMA table_info`                    |
| `quiz_questions` table exists with `quiz_id`, `question_id`, `position` | PASS   | `test_quiz_questions_table_columns`                                                      |
| Existing `questions` table and data are unaffected                      | PASS   | `test_questions_table_unaffected`, `test_migration_is_idempotent` (data survives re-run) |

### Test Output

```
$ python -m pytest tests/ -q
............................................................             [100%]
60 passed in 1.09s

# Fresh start inspection (create_app on empty data/quiz_bank.db):
user_version: 2
tables: ['questions', 'quiz_questions', 'quizzes']
quizzes        -> [('id','INTEGER'), ('name','TEXT'), ('created_at','TEXT')]
quiz_questions -> [('quiz_id','INTEGER'), ('question_id','INTEGER'), ('position','INTEGER')]
```

---

## 5. Known Limitations

* No repository/API layer yet — reading and writing quizzes is `o02/t02`.
* `quizzes` intentionally has no `description` column: the objective marks quiz
  metadata beyond `name` as out of scope, and the task specifies only
  `id`, `name`, `created_at`. (Note: `ui-spec.md` lists an optional quiz
  `description`; it is deliberately not persisted in V2 per the objective.)

---

## 6. Next Suggested Task

**Next task:** `o02/t02-quiz-api`
**Context:** Schema v2 is live. A `QuizRepository` + `/api/quizzes` blueprint
should build on this join table: store ordered `questionIds` as
`quiz_questions` rows (position = index), enforce the min-3-questions rule
(objective validation), and reject saving otherwise with a clear error. Follow
the V1 pattern: repository takes an optional `db_path`, the blueprint reads its
repo from `app.config`, and validation errors surface as a `400` body. Register
the new blueprint in `create_app` alongside `questions_bp`.
