# Evidence: Add Exam Attempts Schema and Repository

**ID:** o03-e01-add-exam-attempts-schema
**Task Ref:** `.devflow/tasks/o03/t01-add-exam-attempts-schema.md`
**Executed By:** Cursor
**Execution Date:** 2026-07-09
**Execution Time:** ~13:47 UTC+8
**Status:** completed

---

## 1. Summary

Added SQLite migration v3 for exam persistence (`exam_attempts`, `exam_answers`), introduced `ExamAttempt` and `ExamAnswer` dataclasses, and implemented `ExamAttemptRepository` with create/save/submit/read operations. All repository unit tests pass and the full existing test suite remains green.

---

## 2. Files Changed

| File                            | Change Type | Description                                |
| ------------------------------- | ----------- | ------------------------------------------ |
| `backend/db.py`                 | modified    | Migration v3, `SCHEMA_VERSION = 3`         |
| `backend/models.py`             | created     | `ExamAttempt` and `ExamAnswer` dataclasses |
| `backend/exam_repository.py`    | created     | Exam attempt repository layer              |
| `tests/test_exam_repository.py` | created     | Repository unit tests (9 tests)            |

---

## 3. Behavior Added

* `exam_attempts` table stores quiz reference, score/total (set on submit), and timestamps
* `exam_answers` table stores per-question selections with upsert via `ON CONFLICT`
* `ExamAttemptRepository.create_attempt(quiz_id)` creates a pending attempt
* `save_answer` inserts or replaces answers before submission
* `submit_attempt` records score, total, and `submitted_at`
* `get_attempt_with_answers` returns attempt plus answer rows

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                      | Result | Notes                               |
| ---------------------------------------------- | ------ | ----------------------------------- |
| Tables created on fresh database               | PASS   | Migration v3                        |
| `create_attempt` returns pending attempt       | PASS   | `submitted_at` and `score` are NULL |
| `save_answer` inserts/replaces                 | PASS   | Upsert tested                       |
| `submit_attempt` sets score and timestamp      | PASS   |                                     |
| `get_attempt_with_answers` returns full record | PASS   |                                     |
| Repository unit tests pass                     | PASS   | 9/9                                 |
| `init_database()` still bootstraps cleanly     | PASS   | Full suite 72/72                    |

### Test Output

```
72 passed in 1.30s
```

---

## 5. Known Limitations

* No API routes yet — persistence layer only (t02 adds REST endpoints).
* No frontend changes in this task.

---

## 6. Next Suggested Task

**Next task:** `o03/t02-implement-exam-api`
**Context:** Wire `ExamAttemptRepository` into `/api/exams/attempts` endpoints with scoring on submit.
