# Evidence: Implement Exam API Endpoints

**ID:** o03-e02-implement-exam-api
**Task Ref:** `.devflow/tasks/o03/t02-implement-exam-api.md`
**Executed By:** Cursor
**Execution Date:** 2026-07-09
**Execution Time:** ~13:56 UTC+8
**Status:** completed

---

## 1. Summary

Exposed the exam flow through REST API endpoints for starting attempts, saving answers, and submitting for scoring. Scoring compares saved answers against quiz questions and returns a full answer review payload on submit. All API tests pass and the full regression suite remains green.

---

## 2. Files Changed

| File                      | Change Type | Description                                          |
| ------------------------- | ----------- | ---------------------------------------------------- |
| `backend/routes/exams.py` | created     | Exam API blueprint with create/save/submit endpoints |
| `backend/app.py`          | modified    | Registered `exams_bp`                                |
| `tests/test_exam_api.py`  | created     | API integration tests (10 tests)                     |

---

## 3. Behavior Added

* `POST /api/exams/attempts` — create attempt for `quiz_id`, returns `attempt_id` (201)
* `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}` — save/update answer (204)
* `POST /api/exams/attempts/{attempt_id}/submit` — score and return summary with answer review
* Scoring counts correct matches; unanswered questions score as incorrect
* Submit returns 409 if already submitted; invalid quiz/attempt/question returns 404
* Correct answers only exposed in submit response

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                       | Result | Notes                              |
| ----------------------------------------------- | ------ | ---------------------------------- |
| Create attempt returns 201 + attempt_id         | PASS   |                                    |
| Save answer returns 204                         | PASS   |                                    |
| Submit returns score summary with answer review | PASS   | Includes question text and options |
| Resubmit returns 409                            | PASS   |                                    |
| Invalid quiz/attempt returns 404                | PASS   |                                    |
| Full regression green                           | PASS   | 82/82                              |

### Test Output

```
82 passed in 1.59s
```

---

## 5. Known Limitations

* No frontend UI yet — API only.
* `GET /api/exams` list endpoint not implemented (frontend uses `GET /api/quizzes`).

---

## 6. Next Suggested Task

**Next task:** `o03/t03-build-available-exams-page`
**Context:** Enable Online Exam navigation and build the Available Exams listing page using `GET /api/quizzes`.
