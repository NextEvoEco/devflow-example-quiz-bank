# Evidence: Implement Exam API Endpoints

**ID:** o03-e02-implement-exam-api
**Task Ref:** `.devflow/tasks/o03/t02-implement-exam-api.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Status:** completed

---

## 1. Summary

Implemented the Online Exam HTTP layer by adding an `exams` blueprint with attempt creation, per-question answer saving, and attempt submission/scoring. Wired the blueprint into the Flask app and added API tests covering the happy path plus required 404 and 409 error behavior.

---

## 2. Files Changed

| File                         | Change Type | Description                                                                                            |
| ---------------------------- | ----------- | ------------------------------------------------------------------------------------------------------ |
| `backend/routes/__init__.py` | created     | Added route package marker for new blueprints.                                                         |
| `backend/routes/exams.py`    | created     | Added Online Exam routes, validation, scoring, and error handling.                                     |
| `backend/app.py`             | modified    | Registered the new exam blueprint with the Flask app.                                                  |
| `tests/test_exam_api.py`     | created     | Added API tests for attempt creation, answer saving, submission scoring, and conflict/not-found cases. |
| `.devflow/status.md`         | modified    | Advanced runtime state to `o03/t02`, then marked it verified and pointed to `o03/t03`.                 |

---

## 3. Behavior Added

* `POST /api/exams/attempts` creates an attempt for an existing quiz and returns `{"attempt_id": <int>}` with status 201.
* `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}` saves or updates one answer and returns 204.
* `POST /api/exams/attempts/{attempt_id}/submit` scores the attempt, persists `score`, `total`, and `submitted_at`, and returns answer review data.
* Submit responses now include `question_text` and option labels so the future frontend does not need extra answer-review fetches.
* Re-submitting an already submitted attempt now returns 409 Conflict.
* Invalid quiz IDs and attempt IDs now return 404 responses with consistent JSON error payloads.

---

## 4. Acceptance Criteria Check

| Criterion                                                                                                | Result | Notes                                                                                                                                                                         |
| -------------------------------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `POST /api/exams/attempts` with a valid `quiz_id` returns `{"attempt_id": <int>}` and 201                | PASS   | Covered by `test_create_attempt_returns_attempt_id`.                                                                                                                          |
| `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}` with `{"selected_option": "A"}` returns 204 | PASS   | Covered by `test_save_answer_returns_204`.                                                                                                                                    |
| Submit returns `{score, total, percentage, answers[...]}` with answer review data                        | PASS   | Covered by `test_submit_attempt_returns_score_summary_and_answer_review`.                                                                                                     |
| Submitting an already submitted attempt returns 409                                                      | PASS   | Covered by `test_submit_attempt_returns_409_when_already_submitted`.                                                                                                          |
| Invalid `attempt_id` or `quiz_id` returns 404                                                            | PASS   | Covered by `test_create_attempt_returns_404_for_missing_quiz`, `test_save_answer_returns_404_for_missing_attempt`, and `test_submit_attempt_returns_404_for_missing_attempt`. |
| Exam API tests and existing regression suite remain green                                                | PASS   | Verified with targeted and full test runs.                                                                                                                                    |

---

## 5. Verification

```text
py -m pytest tests/test_exam_api.py -v
7 passed in 0.29s

py -m pytest tests -v
55 passed in 1.50s
```

---

## 6. Notes

* The repository's live architecture still uses a mostly centralized `backend/app.py`, so I introduced a new `exams` blueprint without refactoring the existing question/quiz endpoints into blueprints. That keeps this task within scope and avoids incidental changes to V1/V2 routes.
* The route accepts both `quiz_id`/`selected_option` and camelCase aliases to stay tolerant of the app's mixed external naming conventions.

---

## 7. Next Suggested Task

**Next task:** `o03/t03-build-available-exams-page`
