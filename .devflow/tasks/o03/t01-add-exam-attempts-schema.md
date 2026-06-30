# Task: Add Exam Attempts Schema and Repository

**ID:** o03/t01-add-exam-attempts-schema
**File:** `.devflow/tasks/o03/t01-add-exam-attempts-schema.md`
**Objective Ref:** `.devflow/objective/o03-online-exam-v1.md`
**Depends On:** none
**Complexity:** S
**Estimated Duration:** 30 min
**Status:** verified

---

## 1. Purpose

Add the database schema for exam attempts and a repository layer to create and read attempts. This task produces no UI and no API routes — only the persistence foundation that later tasks will build on.

---

## 2. Boundary

### In Scope

* Add migration for `exam_attempts` table (id, quiz_id, score, total, started_at, submitted_at).
* Add migration for `exam_answers` table (id, attempt_id, question_id, selected_option).
* Add `ExamAttempt` and `ExamAnswer` model dataclasses.
* Add `ExamAttemptRepository` with methods: `create_attempt`, `save_answer`, `get_attempt_with_answers`, `submit_attempt`.
* Unit tests for the repository layer using a temporary in-memory SQLite database.

### Out of Scope

* API routes.
* Frontend code.
* Any Quiz Builder or Question Bank schema changes.

---

## 3. Must / Must Not

### Must

* Follow the existing migration pattern in `backend/database.py`.
* Increment `SCHEMA_VERSION` correctly.
* Keep `exam_answers.selected_option` nullable to allow unanswered questions at submit time.
* A submitted attempt must record `submitted_at` and `score`; a pending attempt has both as NULL.

### Must Not

* Modify existing `questions` or quiz-related tables.
* Add routes or any HTTP-layer code in this task.

---

## 4. Inputs

| Artifact                    | Source                                     |
| --------------------------- | ------------------------------------------ |
| Existing migration pattern  | `backend/database.py`                      |
| Existing model pattern      | `backend/models.py`                        |
| Existing repository pattern | `backend/question_repository.py`           |
| Objective scope             | `.devflow/objective/o03-online-exam-v1.md` |

---

## 5. Outputs

| Artifact                    | Path                            |
| --------------------------- | ------------------------------- |
| Updated schema migrations   | `backend/database.py`           |
| New model dataclasses       | `backend/models.py`             |
| New exam attempt repository | `backend/exam_repository.py`    |
| Repository unit tests       | `tests/test_exam_repository.py` |

---

## 6. Acceptance Criteria

* [x] `exam_attempts` and `exam_answers` tables are created by the migration on a fresh database.
* [x] `create_attempt(quiz_id)` returns a new attempt with `submitted_at = NULL`.
* [x] `save_answer(attempt_id, question_id, selected_option)` inserts or replaces the answer row.
* [x] `submit_attempt(attempt_id, score, total)` sets `submitted_at` and `score`.
* [x] `get_attempt_with_answers(attempt_id)` returns the attempt and all its answer rows.
* [x] All repository unit tests pass against a temporary in-memory database.
* [x] Existing `initialize_database()` call still bootstraps all tables without error.

---

## 7. Test Plan

```
pytest tests/test_exam_repository.py -v
python -m backend  # verify app still starts and existing tables intact
```

---

## 8. Notes

Use `INSERT OR REPLACE` for `save_answer` to handle answer changes before submission.
`score` should be stored as an integer (number of correct answers); percentage is calculated at display time.
