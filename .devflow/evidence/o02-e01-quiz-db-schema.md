# Evidence: Quiz Database Schema

**ID:** o02-e01-quiz-db-schema
**Task Ref:** `.devflow/tasks/o02/t01-quiz-db-schema.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** ~15:30 UTC+8 (implementation pass)
**Status:** completed

---

## 1. Summary

Added Flyway migration `V3__create_quizzes.sql` creating `quizzes` (`id`, `name`,
`created_at`) and `quiz_questions` (`quiz_id`, `question_id`, `position`) with foreign
keys and ordered positions. Existing `questions` table unchanged. Verified by app
startup / Flyway migrate to version 3 and subsequent `./mvnw test`.

---

## 2. Files Changed

| File                                                             | Change Type | Description                     |
| ---------------------------------------------------------------- | ----------- | ------------------------------- |
| `backend/src/main/resources/db/migration/V3__create_quizzes.sql` | created     | quizzes + quiz_questions schema |

---

## 3. Behavior Added

* PostgreSQL can store quizzes and ordered question references.
* Flyway applies quiz schema automatically on startup after V1/V2.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                           | Result | Notes                           |
| --------------------------------------------------- | ------ | ------------------------------- |
| App starts without errors after schema change       | PASS   | Flyway migrated to v3           |
| `quizzes` has id, name, created_at                  | PASS   | migration DDL                   |
| `quiz_questions` has quiz_id, question_id, position | PASS   | FKs + UNIQUE(quiz_id, position) |
| Existing `questions` unaffected                     | PASS   | no ALTER on questions           |

### Test Output

```
Flyway: Migrating schema "public" to version "3 - create quizzes"
./mvnw test → BUILD SUCCESS (later suite includes quiz tests on this schema)
```

---

## 5. Known Limitations

* No quiz API or UI yet (o02/t02+).

---

## 6. Next Suggested Task

**Next task:** `o02/t02-quiz-api`
**Context:** Implement QuizRepository + `/api/quizzes` CRUD with min-3 validation.
