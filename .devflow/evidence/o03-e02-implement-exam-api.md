# Evidence: Implement Exam API Endpoints

**ID:** o03-e02-implement-exam-api
**Task Ref:** `.devflow/tasks/o03/t02-implement-exam-api.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~45 min
**Status:** completed

---

## 1. Summary

Exposed the exam flow through a `/api/exams` Flask blueprint over the t01
attempt repository, following the V1/V2 pattern (repository on `app.config`,
blueprint reads it via `current_app`). Three endpoints: create an attempt for a
quiz, save/update one answer, and submit for scoring. Scoring compares each saved
`selected_option` to the question's `correct` and counts matches; unanswered
questions count as wrong. Submit is idempotent-safe (409 if already submitted)
and correct answers are never returned before submission — only the submit
response includes `correct_option`, plus `question_text` and option labels so the
frontend can render Answer Review without extra calls. No V1/V2 routes were
modified. Verified with 120 passing tests (13 new) and a live curl walkthrough.

---

## 2. Files Changed

| File                         | Change Type | Description                                                                                                        |
| ---------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------ |
| `backend/routes/exams.py`    | created     | `/api/exams` blueprint: create attempt, save answer, submit+score; error mapping                                   |
| `backend/routes/__init__.py` | modified    | export `exams_bp`                                                                                                  |
| `backend/app.py`             | modified    | build `ExamAttemptRepository`, store on `app.config`, register `exams_bp` (V1/V2 wiring untouched)                 |
| `tests/test_exam_api.py`     | created     | 13 API tests: create/save/submit happy paths + error cases + regression                                            |
| `tests/test_v1_release.py`   | modified    | Removed the now-obsolete `/api/exams`-absent guard (exam API is in-scope in V3); kept exam page-views-absent guard |
| `tests/test_o02_release.py`  | modified    | Same: dropped the `/api/exams`-absent assertion, kept exam page-views-absent                                       |

---

## 3. Behavior Added

* `POST /api/exams/attempts` `{quiz_id}` → `201 {"attempt_id": <int>}`; `404` if the quiz doesn't exist; `400` if `quiz_id` missing/non-integer.
* `PUT /api/exams/attempts/<attempt_id>/answers/<question_id>` `{selected_option}` → `204`; `404` for an unknown attempt or a question not in the attempt's quiz; `400` for an invalid option.
* `POST /api/exams/attempts/<attempt_id>/submit` → `200` with `{score, total, percentage, answers:[{question_id, question_text, options, selected_option, correct_option, is_correct}]}`; `409` if already submitted; `404` for an unknown attempt.
* Scoring: correct count vs each question's `correct`; unanswered = wrong; percentage = `round(score/total*100)`.
* Abandoned attempts (never submitted) stay pending — no scored rows are written.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                        | Result | Notes                                                                                             |
| -------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------- |
| `POST /api/exams/attempts` with valid `quiz_id` returns `{"attempt_id"}` and 201 | PASS   | test + curl                                                                                       |
| `PUT .../answers/{question_id}` with `{"selected_option":"A"}` returns 204       | PASS   | test + curl                                                                                       |
| `POST .../submit` returns `{score, total, percentage, answers:[...]}`            | PASS   | curl: score 2, total 3, percentage 67; review has correct_option/is_correct/question_text/options |
| Submitting an already-submitted attempt returns 409                              | PASS   | `test_submit_already_submitted_returns_409` + curl                                                |
| Invalid `attempt_id` or `quiz_id` returns 404                                    | PASS   | bad-quiz create → 404; bad-attempt submit → 404                                                   |
| All API tests pass; existing question and quiz API tests remain green            | PASS   | full suite 120 green                                                                              |

### Test Output

```
$ python -m pytest -q
120 passed in 3.37s

# Live curl (3 questions correct A/B/C, quiz over them):
POST /api/exams/attempts {quiz_id}            -> 201 {"attempt_id":N} (no "correct" in body)
PUT  .../answers/{q1..q3} {selected_option}   -> 204, 204, 204
POST .../submit                               -> 200 {score:2, total:3, percentage:67,
                                                     answers:[... correct_option, is_correct, question_text, options]}
POST .../submit (again)                       -> 409
POST /api/exams/attempts {quiz_id:9999}       -> 404
POST /api/exams/attempts/9999/submit          -> 404
```

---

## 5. Known Limitations

* No exam-taking content endpoint yet: the exam-taking page (o03/t04) will need
  question text/options **without** correct answers. The existing
  `GET /api/quizzes/<id>` returns `correct` (V2 behavior we must not change), so
  the frontend must avoid displaying it during the exam, or a future task may add
  an exam-safe question endpoint. The new `/api/exams` endpoints themselves never
  reveal `correct` before submit.
* Answers can still be PUT after submit (harmless — re-submit is 409, so the
  recorded score is fixed); not blocked since the task doesn't require it.

---

## 6. Next Suggested Task

**Next task:** `o03/t03-build-available-exams-page`
**Context:** The exam API is ready. t03 builds the `examList` page: activate the
Online Exam sidebar nav item (currently a disabled placeholder), render all
quizzes as exam cards (name, question count, "Start Exam") from the existing
`GET /api/quizzes`, and on Start Exam create an attempt via
`POST /api/exams/attempts` and navigate to `examTaking` (built in o03/t04). Use
the shared nav controller (`registerPage`, `navigate` — see `.devflow/memory.md`).
Exam content sourcing (questions without correct answers) is an o03/t04 concern —
see the limitation above.
