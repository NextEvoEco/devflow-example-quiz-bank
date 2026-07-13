# Evidence: Add Exam Attempts Schema and Repository

**ID:** o03-e01-add-exam-attempts-schema
**Task Ref:** `.devflow/tasks/o03/t01-add-exam-attempts-schema.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-11
**Status:** completed

## 1. Summary

Added SCHEMA_VERSION 3 (`exam_attempts`, `exam_answers`), dataclasses, and `ExamAttemptRepository`.

## 2. Files Changed

| File                            | Change Type | Description            |
| ------------------------------- | ----------- | ---------------------- |
| `backend/database.py`           | modified    | v3 migration           |
| `backend/models.py`             | modified    | ExamAttempt/ExamAnswer |
| `backend/exam_repository.py`    | created     | Repository             |
| `tests/test_exam_repository.py` | created     | Unit tests             |

## 3. Behavior Added

* Create/save/submit/get attempt persistence

## 4. Test Results

PASS via `test_exam_repository_flow`

## 5. Known Limitations

* None

## 6. Next Suggested Task

**Next task:** `o03/t02-implement-exam-api`
