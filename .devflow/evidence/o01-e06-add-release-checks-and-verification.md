# Evidence: Add Release Checks And Verification

**ID:** o01-e06-add-release-checks-and-verification
**Task Ref:** `.devflow/tasks/o01/t06-add-release-checks-and-verification.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** 15:29-15:30 UTC+8, ~10 min
**Status:** completed

---

## 1. Summary

Completed V1 release verification: README startup/test instructions updated,
`ReleaseSmokeTest` added, full `./mvnw test` and `npm test` green, and black-box
HTTP smoke against the running app (`/api/health`, SPA `/`, `/api/questions`).
Quiz Builder / Online Exam remain out of V1 scope.

---

## 2. Files Changed

| File                                                           | Change Type | Description                      |
| -------------------------------------------------------------- | ----------- | -------------------------------- |
| `README.md`                                                    | modified    | runnable start/test instructions |
| `backend/src/test/java/com/quizbank/web/ReleaseSmokeTest.java` | created     | V1 release smoke tests           |

---

## 3. Behavior Added

* Documented local start and verification path for a fresh session.
* Automated release smoke covering health, SPA index, and question CRUD baseline.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                       | Result | Notes                       |
| ----------------------------------------------- | ------ | --------------------------- |
| App starts and demonstrates as V1 Question Bank | PASS   | running on :5000            |
| Automated tests cover V1 baseline               | PASS   | mvnw test + npm test        |
| Startup/verification documented                 | PASS   | README + installation-guide |
| Quiz Builder / Online Exam excluded             | PASS   | only Question Bank nav/UI   |

### Test Output

```
./mvnw test → BUILD SUCCESS
npm test → 2 passed
GET /api/health → ok
GET / → 200 Quiz Bank
GET /api/questions → 200
```

---

## 5. Known Limitations

* Seed import from `data/quiz_bank.db` still deferred (see memory.md).

---

## 6. Next Suggested Task

**Next task:** `o02/t01-quiz-db-schema`
**Context:** Begin Quiz Builder objective; add `quizzes` + `quiz_questions` Flyway migration.
