# Evidence: Add Exam Attempts Schema and Repository

**ID:** o03-e01-add-exam-attempts-schema
**Task Ref:** `.devflow/tasks/o03/t01-add-exam-attempts-schema.md`
**Executed By:** Cursor
**Execution Date:** 2026-06-30
**Execution Time:** ~30 min
**Status:** completed

---

## 1. Summary

Added migration v4 for `exam_attempts` and `exam_answers` tables, `ExamAttempt` / `ExamAnswer` model dataclasses, and `ExamAttemptRepository` with create, save, submit, and read methods. Repository unit tests pass against in-memory SQLite; the full test suite (75 tests) passes and the app still starts cleanly.

---

## 2. Files Changed

| File                                                 | Change Type | Description                                                 |
| ---------------------------------------------------- | ----------- | ----------------------------------------------------------- |
| `backend/database.py`                                | modified    | Added migration v4; `SCHEMA_VERSION` set to 4               |
| `backend/models.py`                                  | modified    | Added `ExamAttempt`, `ExamAnswer`, `ExamAttemptWithAnswers` |
| `backend/exam_repository.py`                         | created     | Exam attempt persistence layer                              |
| `tests/test_exam_repository.py`                      | created     | Repository and schema verification tests                    |
| `tests/test_bootstrap.py`                            | modified    | Assert migration v4 tables on fresh init                    |
| `.devflow/status.md`                                 | modified    | Updated runtime state after task completion                 |
| `.devflow/tasks/o03/t01-add-exam-attempts-schema.md` | modified    | Marked task verified                                        |
| `.devflow/memory.md`                                 | modified    | Added migration v4 handoff note                             |

---

## 3. Behavior Added

* `exam_attempts` table with `id`, `quiz_id`, `score`, `total`, `started_at`, `submitted_at`
* `exam_answers` table with `id`, `attempt_id`, `question_id`, `selected_option` (nullable)
* `UNIQUE (attempt_id, question_id)` to support `INSERT OR REPLACE` on answer updates
* Foreign keys to `quizzes`, `exam_attempts`, and `questions` with `ON DELETE CASCADE`
* `ExamAttemptRepository.create_attempt`, `save_answer`, `get_attempt_with_answers`, `submit_attempt`

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                            | Result | Notes                                                   |
| -------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| `exam_attempts` and `exam_answers` tables created on fresh database  | PASS   | `test_fresh_database_includes_exam_tables`              |
| `create_attempt(quiz_id)` returns attempt with `submitted_at = NULL` | PASS   | `test_create_attempt_returns_pending_attempt`           |
| `save_answer` inserts or replaces answer row                         | PASS   | `test_save_answer_inserts_and_replaces`                 |
| `submit_attempt` sets `submitted_at` and `score`                     | PASS   | `test_submit_attempt_sets_score_and_submitted_at`       |
| `get_attempt_with_answers` returns attempt and all answers           | PASS   | `test_get_attempt_with_answers_returns_all_answer_rows` |
| Repository unit tests pass on in-memory SQLite                       | PASS   | 8 tests in `test_exam_repository.py`                    |
| `initialize_database()` bootstraps all tables without error          | PASS   | `test_initialize_database_creates_schema`               |

### Test Output

```
tests/test_exam_repository.py::test_fresh_database_includes_exam_tables PASSED
tests/test_exam_repository.py::test_create_attempt_returns_pending_attempt PASSED
tests/test_exam_repository.py::test_save_answer_inserts_and_replaces PASSED
tests/test_exam_repository.py::test_save_answer_allows_null_selected_option PASSED
tests/test_exam_repository.py::test_submit_attempt_sets_score_and_submitted_at PASSED
tests/test_exam_repository.py::test_get_attempt_with_answers_returns_all_answer_rows PASSED
tests/test_exam_repository.py::test_get_attempt_with_answers_raises_for_missing_attempt PASSED
tests/test_exam_repository.py::test_submit_attempt_raises_for_missing_attempt PASSED

75 passed in full suite
```

---

## 5. Known Limitations

* No API routes or frontend yet; persistence layer only.
* No validation that answers belong to the quiz's question set (deferred to API layer).

---

## 6. Next Suggested Task

**Next task:** `o03/t02-implement-exam-api`
**Context:** Build exam HTTP endpoints on top of `ExamAttemptRepository`; scoring logic will call `submit_attempt` with computed `score` and `total`.
