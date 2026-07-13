# Evidence: Implement Exam API Endpoints

**ID:** o03-e02-implement-exam-api
**Task Ref:** `.devflow/tasks/o03/t02-implement-exam-api.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** ~15:30-15:36 UTC+8 (implementation pass)
**Status:** completed

---

## 1. Summary

Exposed exam REST endpoints via `ExamController`: create attempt, save answer (204),
submit with score summary including review fields. Double-submit returns 409; invalid
ids return 404. Covered by `ExamApiTest`; question/quiz tests remain green.

---

## 2. Files Changed

| File                                                              | Change Type | Description      |
| ----------------------------------------------------------------- | ----------- | ---------------- |
| `backend/src/main/java/com/quizbank/web/ExamController.java`      | created     | exam routes      |
| `backend/src/main/java/com/quizbank/web/ConflictException.java`   | created     | 409 mapping      |
| `backend/src/main/java/com/quizbank/web/ApiExceptionHandler.java` | modified    | conflict handler |
| `backend/src/test/java/com/quizbank/web/ExamApiTest.java`         | created     | exam API tests   |

---

## 3. Behavior Added

* `POST /api/exams/attempts` → `{attempt_id}` (201)
* `PUT .../answers/{question_id}` → 204
* `POST .../submit` → score/total/percentage/answers review payload
* Scoring compares selected_option to questions.correct

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                 | Result | Notes                         |
| ----------------------------------------- | ------ | ----------------------------- |
| POST attempts valid quiz → 201 attempt_id | PASS   | ExamApiTest                   |
| PUT answer → 204                          | PASS   |                               |
| POST submit returns score summary         | PASS   | includes options + is_correct |
| Double submit → 409                       | PASS   |                               |
| Invalid attempt/quiz → 404                | PASS   |                               |
| All API tests pass; question/quiz green   | PASS   | full suite                    |

### Test Output

```
./mvnw test → BUILD SUCCESS (includes ExamApiTest)
Black-box smoke: attempt → answers → submit → score 3/3 (100%)
```

---

## 5. Known Limitations

* No exam history listing endpoints (out of scope).

---

## 6. Next Suggested Task

**Next task:** `o03/t03-build-available-exams-page`
**Context:** Add Online Exam sidebar + list cards from GET /api/quizzes.
