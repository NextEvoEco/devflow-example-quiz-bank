# Evidence: Add Exam Attempts Schema and Repository

**ID:** o03-e01-add-exam-attempts-schema
**Task Ref:** `.devflow/tasks/o03/t01-add-exam-attempts-schema.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~30 min
**Status:** completed

---

## 1. Summary

Laid the persistence foundation for Online Exam V3. Extended the versioned SQLite
migration to schema v3 with two tables — `exam_attempts` (id, quiz_id, score,
total, started_at, submitted_at) and `exam_answers` (id, attempt_id, question_id,
selected_option) — added `ExamAttempt` / `ExamAnswer` dataclasses, and an
`ExamAttemptRepository` with `create_attempt`, `save_answer` (insert-or-replace),
`submit_attempt`, and `get_attempt_with_answers`. Pending attempts keep
score/total/submitted_at NULL; `selected_option` is nullable so unanswered
questions can be recorded. No API or frontend code, and no changes to the
questions or quiz tables. Verified with 109 passing tests (11 new) and a
fresh-start inspection showing `user_version = 3` and correct nullability.

---

## 2. Files Changed

| File                            | Change Type | Description                                                                                                 |
| ------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------- |
| `backend/database.py`           | modified    | `SCHEMA_VERSION` → 3; added `exam_attempts` + `exam_answers` DDL and a `version < 3` migration step         |
| `backend/models.py`             | modified    | Added `ExamAttempt` / `ExamAnswer` dataclasses + row mappers                                                |
| `backend/exam_repository.py`    | created     | `ExamAttemptRepository`: create_attempt, get_attempt, save_answer, submit_attempt, get_attempt_with_answers |
| `tests/test_exam_repository.py` | created     | 11 tests: schema, pending create, save/replace/null answer, submit, get-with-answers, missing cases         |
| `tests/test_quiz_schema.py`     | modified    | Relaxed two version assertions from `== 2` to `>= 2` so later migrations don't break them                   |

---

## 3. Behavior Added

* On startup, a database at schema v2 (or fresh) migrates to v3 by creating
  `exam_attempts` and `exam_answers`; a v3 database is left as-is.
* `create_attempt(quiz_id)` inserts a pending attempt (score/total/submitted_at NULL).
* `save_answer(attempt_id, question_id, selected_option)` inserts or replaces the
  row for that question (via `UNIQUE(attempt_id, question_id)` + `INSERT OR REPLACE`);
  `selected_option` may be NULL.
* `submit_attempt(attempt_id, score, total)` sets score, total, and `submitted_at`.
* `get_attempt_with_answers(attempt_id)` returns the attempt with an `answers` list.
* Cascades: deleting a quiz removes its attempts; deleting an attempt removes its
  answers; deleting a referenced question removes matching answer rows.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                  | Result | Notes                                                                           |
| -------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------- |
| `exam_attempts` and `exam_answers` created by the migration on a fresh DB  | PASS   | `test_migration_creates_exam_tables`; fresh-start inspection                    |
| `create_attempt(quiz_id)` returns a new attempt with `submitted_at = NULL` | PASS   | `test_create_attempt_is_pending` (score/total also NULL)                        |
| `save_answer(...)` inserts or replaces the answer row                      | PASS   | `test_save_answer_inserts`, `test_save_answer_replaces_existing` (no duplicate) |
| `submit_attempt(attempt_id, score, total)` sets `submitted_at` and `score` | PASS   | `test_submit_attempt_sets_score_and_timestamp`                                  |
| `get_attempt_with_answers(attempt_id)` returns attempt + all answer rows   | PASS   | `test_get_attempt_with_answers_returns_all`                                     |
| All repository unit tests pass against a temporary DB                      | PASS   | 11/11 in `test_exam_repository.py`                                              |
| Existing DB bootstrap still creates all tables without error               | PASS   | `create_app()` on fresh DB → 5 tables, `user_version = 3`                       |

### Test Output

```
$ python -m pytest tests/ -q
109 passed in 2.71s

# Fresh start inspection (create_app on empty data/quiz_bank.db):
user_version: 3
tables: ['exam_answers', 'exam_attempts', 'questions', 'quiz_questions', 'quizzes']
exam_attempts  -> id, quiz_id(NOT NULL), score(NULL), total(NULL), started_at(NOT NULL), submitted_at(NULL)
exam_answers   -> id, attempt_id(NOT NULL), question_id(NOT NULL), selected_option(NULL)
```

---

## 5. Known Limitations

* No API or UI yet — routes are `o03/t02`, pages are `o03/t03`–`t05`.
* Scoring is not computed here; `submit_attempt` records a score passed by the
  caller (the API/exam-taking layer computes correctness). `score` is an integer
  count; percentage is derived at display time.
* The task text references `initialize_database()`; the actual bootstrap function
  is `init_db()` (called by `create_app`). No rename was made — the existing
  bootstrap continues to create all tables.

---

## 6. Next Suggested Task

**Next task:** `o03/t02-implement-exam-api`
**Context:** Schema v3 and `ExamAttemptRepository` are ready. The `/api/exams`
blueprint should: start an attempt for a quiz (`create_attempt`), save answers
as the user selects (`save_answer`), and submit (compute score by comparing
`selected_option` to each question's `correct`, then `submit_attempt`). Exam
content comes from `GET /api/quizzes/<id>` (ordered questions with correct
answers). Follow the V1/V2 pattern: repository on `app.config`, blueprint reads
it via `current_app`, register in `create_app` alongside `questions_bp` /
`quizzes_bp`. Note: correct answers must only be revealed at results time
(objective: single formal exam mode) — design the "exam-taking" responses to
omit `correct` until submission.
