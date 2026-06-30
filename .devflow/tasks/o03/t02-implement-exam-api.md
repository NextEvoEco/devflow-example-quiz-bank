# Task: Implement Exam API Endpoints

**ID:** o03/t02-implement-exam-api
**File:** `.devflow/tasks/o03/t02-implement-exam-api.md`
**Objective Ref:** `.devflow/objective/o03-online-exam-v1.md`
**Depends On:** o03/t01-add-exam-attempts-schema
**Complexity:** M
**Estimated Duration:** 45 min
**Status:** verified

---

## 1. Purpose

Expose the exam flow through REST API endpoints: starting an attempt, saving an answer, and submitting the attempt for scoring. The frontend can call these endpoints without knowing the scoring or persistence logic.

---

## 2. Boundary

### In Scope

* `POST /api/exams/attempts` — create a new attempt for a given `quiz_id`; return `attempt_id`.
* `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}` — save or update one answer; return 204.
* `POST /api/exams/attempts/{attempt_id}/submit` — score and persist the attempt; return score summary.
* Register the new blueprint in `backend/app.py`.
* API-level tests covering the happy path and basic error cases (invalid quiz_id, invalid attempt_id, submitting an already-submitted attempt).

### Out of Scope

* Frontend code.
* Listing available exams (the frontend will call the existing `GET /api/quizzes` endpoint from V2).
* Exam attempt history endpoints.

---

## 3. Must / Must Not

### Must

* Scoring logic: compare each `exam_answers.selected_option` against the corresponding `questions.correct`; count matches.
* `submit` must be idempotent-safe: if `submitted_at` is already set, return 409 Conflict.
* Abandoned attempts (no `submit` call) must never be partially written as scored rows.

### Must Not

* Modify any existing V1 or V2 routes.
* Return correct answers in any response before submission (only return them as part of the submit response).

---

## 4. Inputs

| Artifact                   | Source                                     |
| -------------------------- | ------------------------------------------ |
| Exam repository            | `backend/exam_repository.py` (from t01)    |
| Existing blueprint pattern | `backend/routes/questions.py`              |
| Quiz data (for scoring)    | `backend/question_repository.py`           |
| Objective scope            | `.devflow/objective/o03-online-exam-v1.md` |

---

## 5. Outputs

| Artifact                 | Path                      |
| ------------------------ | ------------------------- |
| Exam routes blueprint    | `backend/routes/exams.py` |
| Updated app registration | `backend/app.py`          |
| API tests                | `tests/test_exam_api.py`  |

---

## 6. Acceptance Criteria

* [x] `POST /api/exams/attempts` with a valid `quiz_id` returns `{"attempt_id": <int>}` and 201.
* [x] `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}` with `{"selected_option": "A"}` returns 204.
* [x] `POST /api/exams/attempts/{attempt_id}/submit` returns score summary: `{score, total, percentage, answers: [{question_id, selected_option, correct_option, is_correct}]}`.
* [x] Submitting an already-submitted attempt returns 409.
* [x] Invalid `attempt_id` or `quiz_id` returns 404.
* [x] All API tests pass; existing question and quiz API tests remain green.

---

## 7. Test Plan

```
pytest tests/test_exam_api.py -v
pytest tests/ -v  # full regression
```

---

## 8. Notes

The submit response `answers` array is what the frontend needs to render the Answer Review section. Include `question_text` and option labels in the response to avoid extra frontend queries.
