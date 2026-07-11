# Evidence: Add Exam Attempts Schema and Repository

**ID:** o03-e01-add-exam-attempts-schema
**Task Ref:** `.devflow/tasks/o03/t01-add-exam-attempts-schema.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Execution Time:** 18:06-18:15 UTC+8, ~9 min
**Status:** completed

---

## 1. Summary

Extended the SQLite schema with Online Exam persistence tables and added an `ExamAttemptRepository` for pending attempts, answer updates, submission state, and full attempt loading. Verified the new repository directly with dedicated tests and confirmed the full existing Question Bank and Quiz Builder baselines still pass after adding schema version 3.

---

## 2. Files Changed

| File                            | Change Type | Description                                                                                                       |
| ------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------- |
| `backend/db.py`                 | modified    | Added schema migration version 3 for `exam_attempts` and `exam_answers`.                                          |
| `backend/exam_repository.py`    | created     | Added `ExamAttempt`, `ExamAnswer`, and `ExamAttemptRepository` with create/save/load/submit methods.              |
| `tests/test_exam_repository.py` | created     | Added repository tests for schema creation, pending attempts, answer replacement, submission, and answer loading. |
| `tests/test_quiz_schema.py`     | modified    | Updated migration-version expectation to include schema version 3.                                                |
| `.devflow/status.md`            | modified    | Moved runtime state to `o03/t01`, then marked it verified and pointed to `o03/t02`.                               |

---

## 3. Behavior Added

* Database bootstrap now creates `exam_attempts` and `exam_answers` on fresh startup.
* Exam attempts can now be created with `submitted_at = NULL`, `score = NULL`, and `total = NULL`.
* Answers can now be inserted or replaced for the same `(attempt_id, question_id)` pair before submission.
* Submitting an attempt now stores `score`, `total`, and `submitted_at`.
* Full attempt loading now returns the attempt and all persisted answer rows.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                                  | Result | Notes                                                                                           |
| ------------------------------------------------------------------------------------------ | ------ | ----------------------------------------------------------------------------------------------- |
| `exam_attempts` and `exam_answers` tables are created by the migration on a fresh database | PASS   | Verified with dedicated repository test and startup schema smoke output.                        |
| `create_attempt(quiz_id)` returns a new attempt with `submitted_at = NULL`                 | PASS   | Covered by `test_create_attempt_returns_pending_attempt`.                                       |
| `save_answer(attempt_id, question_id, selected_option)` inserts or replaces the answer row | PASS   | Covered by `test_save_answer_inserts_or_replaces_answer`.                                       |
| `submit_attempt(attempt_id, score, total)` sets `submitted_at` and `score`                 | PASS   | Covered by `test_submit_attempt_sets_score_total_and_submitted_at`.                             |
| `get_attempt_with_answers(attempt_id)` returns the attempt and all its answer rows         | PASS   | Covered by `test_get_attempt_with_answers_returns_attempt_and_answer_rows`.                     |
| All repository unit tests pass against a temporary in-memory database                      | PASS   | Dedicated repository test suite passed.                                                         |
| Existing `initialize_database()` call still bootstraps all tables without error            | PASS   | Full regression suite passed and startup smoke listed all tables including the new exam tables. |

### Test Output

```text
> py -m pytest tests/test_exam_repository.py -v
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 5 items
tests/test_exam_repository.py::test_exam_attempt_tables_are_created PASSED
tests/test_exam_repository.py::test_create_attempt_returns_pending_attempt PASSED
tests/test_exam_repository.py::test_save_answer_inserts_or_replaces_answer PASSED
tests/test_exam_repository.py::test_submit_attempt_sets_score_total_and_submitted_at PASSED
tests/test_exam_repository.py::test_get_attempt_with_answers_returns_attempt_and_answer_rows PASSED
============================== 5 passed in 0.21s ==============================

> py -m pytest tests -v
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 48 items
============================= 48 passed in 1.15s ==============================

> startup schema smoke
tables -> exam_answers, exam_attempts, questions, quiz_questions, quizzes, schema_migrations
exam_attempts columns -> id, quiz_id, score, total, started_at, submitted_at
exam_answers columns -> id, attempt_id, question_id, selected_option
```

---

## 5. Known Limitations

* This task only adds persistence foundations; there are still no Online Exam API routes or frontend flows.
* I followed the repository's current module layout (`backend/db.py`, repository-per-domain) instead of the older filenames mentioned in the task note (`backend/database.py`, `backend/models.py`), because those files do not exist in the live workspace.

---

## 6. Next Suggested Task

**Next task:** `o03/t02-implement-exam-api`
**Context:** The Online Exam persistence layer is now ready, so the next step can expose attempt creation, answer saving, submission, and results retrieval through HTTP without reworking schema foundations.
