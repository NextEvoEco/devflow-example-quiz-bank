# Evidence: Quiz Database Schema

**ID:** o02-e01-quiz-db-schema
**Task Ref:** `.devflow/tasks/o02/t01-quiz-db-schema.md`
**Executed By:** Cursor
**Execution Date:** 2026-07-09
**Execution Time:** ~10:18 UTC+8
**Status:** completed

---

## 1. Summary

Extended the SQLite schema with migration v2, adding `quizzes` and `quiz_questions` tables for Quiz Builder persistence. The migration runs on app startup after the existing v1 schema and leaves the `questions` table unchanged.

---

## 2. Files Changed

| File                        | Change Type | Description                               |
| --------------------------- | ----------- | ----------------------------------------- |
| `backend/db.py`             | modified    | Added migration v2 for quiz tables        |
| `tests/test_quiz_schema.py` | created     | Schema and foreign key verification tests |

---

## 3. Behavior Added

* `quizzes` table with `id`, `name`, `created_at`
* `quiz_questions` join table with `quiz_id`, `question_id`, `position`
* Foreign keys from `quiz_questions` to `quizzes` and `questions`
* `ON DELETE CASCADE` for quiz and question reference cleanup
* Schema version advanced to `2`

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                           | Result | Notes                               |
| --------------------------------------------------- | ------ | ----------------------------------- |
| App starts without errors after schema change       | PASS   | Health endpoint and full suite pass |
| `quizzes` table exists with required columns        | PASS   | Verified via PRAGMA                 |
| `quiz_questions` table exists with required columns | PASS   | Verified via PRAGMA                 |
| Existing `questions` table unaffected               | PASS   | Column structure unchanged          |

### Test Output

```
37 passed in 0.53s
```

---

## 5. Known Limitations

* No quiz repository or API endpoints yet.
* `quizzes` table does not include `description`; only task-specified columns were added.

---

## 6. Next Suggested Task

**Next task:** `o02/t02-quiz-api`
**Context:** Build `QuizRepository` and `/api/quizzes` endpoints on top of the new schema.
