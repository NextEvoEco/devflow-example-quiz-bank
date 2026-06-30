# Evidence: Implement Exam API Endpoints

**ID:** o03-e02-implement-exam-api
**Task Ref:** `.devflow/tasks/o03/t02-implement-exam-api.md`
**Executed By:** Cursor
**Execution Date:** 2026-06-30
**Execution Time:** ~45 min
**Status:** completed

---

## 1. Summary

Exposed the exam flow through REST endpoints for creating attempts, saving answers, and submitting for scoring. Scoring compares saved answers against quiz questions; submit is idempotent-safe with 409 on repeat submission. All 8 new API tests and the full suite (83 tests) pass.

---

## 2. Files Changed

| File                                           | Change Type | Description                                        |
| ---------------------------------------------- | ----------- | -------------------------------------------------- |
| `backend/routes/exams.py`                      | created     | Exam attempt create, save answer, submit endpoints |
| `backend/app.py`                               | modified    | Registered `exams_bp` and `ExamAttemptRepository`  |
| `tests/test_exam_api.py`                       | created     | Happy path and error-case API tests                |
| `.devflow/status.md`                           | modified    | Updated runtime state after task completion        |
| `.devflow/tasks/o03/t02-implement-exam-api.md` | modified    | Marked task verified                               |
| `.devflow/memory.md`                           | modified    | Added exam API endpoint handoff note               |

---

## 3. Behavior Added

* `POST /api/exams/attempts` — create attempt for `quiz_id`; returns `{"attempt_id": int}` (201)
* `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}` — save/update answer (204)
* `POST /api/exams/attempts/{attempt_id}/submit` — score and return summary with per-question review data
* Submit response includes `score`, `total`, `percentage`, and `answers` with `question_text` and option labels
* 404 for invalid quiz/attempt; 409 for submit or save on already-submitted attempt

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                | Result | Notes                                               |
| -------------------------------------------------------- | ------ | --------------------------------------------------- |
| `POST /api/exams/attempts` returns 201 with `attempt_id` | PASS   | `test_create_attempt_returns_attempt_id`            |
| `PUT .../answers/{question_id}` returns 204              | PASS   | `test_save_answer_returns_204`                      |
| `POST .../submit` returns score summary                  | PASS   | `test_submit_attempt_returns_score_summary`         |
| Already-submitted submit returns 409                     | PASS   | `test_submit_already_submitted_attempt_returns_409` |
| Invalid attempt/quiz returns 404                         | PASS   | Multiple tests                                      |
| Full regression green                                    | PASS   | 83 passed                                           |

### Test Output

```
tests/test_exam_api.py ........                                           [100%]
83 passed in full suite
```

---

## 5. Known Limitations

* No exam attempt history listing endpoint (out of scope).
* Available exams listing still uses existing `GET /api/quizzes` from V2.

---

## 6. Next Suggested Task

**Next task:** `o03/t03-build-available-exams-page`
**Context:** Frontend can list quizzes via `GET /api/quizzes`; starting an exam calls `POST /api/exams/attempts`.
