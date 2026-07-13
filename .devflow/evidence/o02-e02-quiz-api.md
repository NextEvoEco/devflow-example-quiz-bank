# Evidence: Quiz CRUD API

**ID:** o02-e02-quiz-api
**Task Ref:** `.devflow/tasks/o02/t02-quiz-api.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** ~15:30-15:36 UTC+8 (implementation pass)
**Status:** completed

---

## 1. Summary

Implemented quiz persistence and REST API: `Quiz` / `QuizRepository` / `QuizValidator`
and `QuizController` at `/api/quizzes`. Enforces at least three distinct existing
question IDs, preserves `position` order, and returns full question objects on detail
GET. Covered by `QuizApiTest`.

---

## 2. Files Changed

| File                                                                   | Change Type | Description                       |
| ---------------------------------------------------------------------- | ----------- | --------------------------------- |
| `backend/src/main/java/com/quizbank/quiz/Quiz.java`                    | created     | quiz record / JSON shape          |
| `backend/src/main/java/com/quizbank/quiz/QuizRepository.java`          | created     | JdbcTemplate CRUD                 |
| `backend/src/main/java/com/quizbank/quiz/QuizValidator.java`           | created     | min-3 / duplicate checks          |
| `backend/src/main/java/com/quizbank/quiz/QuizValidationException.java` | created     | validation errors                 |
| `backend/src/main/java/com/quizbank/web/QuizController.java`           | created     | REST endpoints                    |
| `backend/src/main/java/com/quizbank/web/ApiExceptionHandler.java`      | modified    | map QuizValidationException → 400 |
| `backend/src/test/java/com/quizbank/web/QuizApiTest.java`              | created     | API success/failure tests         |

---

## 3. Behavior Added

* `GET/POST/PUT/DELETE /api/quizzes`
* Create/update reject &lt;3 questions or unknown question IDs with 400
* Detail GET includes ordered `questions` payloads for preview

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                  | Result | Notes                   |
| ------------------------------------------ | ------ | ----------------------- |
| POST creates quiz → 201                    | PASS   | QuizApiTest             |
| POST with &lt;3 questions → 400            | PASS   | QuizApiTest             |
| POST with non-existent question ID → 400   | PASS   | QuizApiTest             |
| GET list returns quizzes                   | PASS   | includes question_count |
| GET by id returns ordered question objects | PASS   |                         |
| PUT updates name/question list             | PASS   |                         |
| DELETE removes quiz and join rows          | PASS   |                         |
| Question Bank API tests still pass         | PASS   | full `./mvnw test`      |

### Test Output

```
./mvnw test → BUILD SUCCESS (includes QuizApiTest)
```

---

## 5. Known Limitations

* No frontend yet (o02/t03+).
* Quizzes have no persisted description column (UI description is local-only).

---

## 6. Next Suggested Task

**Next task:** `o02/t03-quiz-list-page`
**Context:** Add React Quiz List page and sidebar nav to Quiz Builder.
