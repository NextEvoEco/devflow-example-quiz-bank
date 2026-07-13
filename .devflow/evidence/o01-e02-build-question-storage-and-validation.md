# Evidence: Build Question Storage And Validation

**ID:** o01-e02-build-question-storage-and-validation
**Task Ref:** `.devflow/tasks/o01/t02-build-question-storage-and-validation.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** 15:23-15:25 UTC+8, ~15 min
**Status:** completed

---

## 1. Summary

Added the `questions` table via Flyway `V2__create_questions.sql` (shared logical schema:
`option_a..option_d`, `correct`, `difficulty`). Implemented `Question` model,
`QuestionValidator` (required fields + default difficulty `Medium`), and
`QuestionRepository` (CRUD + case-insensitive search) with JUnit coverage against
PostgreSQL.

---

## 2. Files Changed

| File                                                                           | Change Type | Description                     |
| ------------------------------------------------------------------------------ | ----------- | ------------------------------- |
| `backend/src/main/resources/db/migration/V2__create_questions.sql`             | created     | questions table + index         |
| `backend/src/main/java/com/quizbank/question/Question.java`                    | created     | domain record                   |
| `backend/src/main/java/com/quizbank/question/QuestionValidator.java`           | created     | validation + difficulty default |
| `backend/src/main/java/com/quizbank/question/QuestionValidationException.java` | created     | validation error type           |
| `backend/src/main/java/com/quizbank/question/QuestionRepository.java`          | created     | JdbcTemplate CRUD/search        |
| `backend/src/test/java/com/quizbank/question/QuestionRepositoryTest.java`      | created     | repository integration tests    |
| `backend/src/test/java/com/quizbank/question/QuestionValidatorTest.java`       | created     | unit tests for validator        |

---

## 3. Behavior Added

* Questions can be inserted, updated, deleted, listed, and searched via the repository.
* Invalid payloads raise `QuestionValidationException` with explicit messages.
* Omitted/blank difficulty becomes `Medium`.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                           | Result | Notes                                 |
| ----------------------------------- | ------ | ------------------------------------- |
| CRUD + search via persistence layer | PASS   | Covered by `QuestionRepositoryTest`   |
| Invalid data rejected               | PASS   | blank text / invalid correct rejected |
| Difficulty defaults when omitted    | PASS   | defaults to Medium                    |

### Test Output

```
./mvnw test → BUILD SUCCESS
Flyway migrated schema public to version "2 - create questions"
```

---

## 5. Known Limitations

* No HTTP API yet (o01/t03).
* Repository tests share the local `quiz_bank` database (clean `questions` before each test).

---

## 6. Next Suggested Task

**Next task:** `o01/t03-implement-question-bank-api`
**Context:** Expose `/api/questions` REST endpoints on top of `QuestionRepository`; map validation/not-found to explicit error responses.
