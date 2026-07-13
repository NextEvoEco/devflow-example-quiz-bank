# Evidence: Add Exam Attempts Schema and Repository

**ID:** o03-e01-add-exam-attempts-schema
**Task Ref:** `.devflow/tasks/o03/t01-add-exam-attempts-schema.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** ~15:30-15:36 UTC+8 (implementation pass)
**Status:** completed

---

## 1. Summary

Added Flyway `V4__create_exam_attempts.sql` for `exam_attempts` and `exam_answers`,
plus `ExamAttemptRepository` with create/save/get/submit helpers. Pending attempts keep
`submitted_at` and `score` null; `selected_option` is nullable. No HTTP routes in this
task boundary (routes added in t02).

---

## 2. Files Changed

| File                                                                   | Change Type | Description                   |
| ---------------------------------------------------------------------- | ----------- | ----------------------------- |
| `backend/src/main/resources/db/migration/V4__create_exam_attempts.sql` | created     | exam tables                   |
| `backend/src/main/java/com/quizbank/exam/ExamAttemptRepository.java`   | created     | persistence + scoring helpers |

---

## 3. Behavior Added

* Schema supports exam attempts and per-question answers.
* Repository can create attempts, upsert answers, and submit scores.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                          | Result | Notes                                       |
| ---------------------------------- | ------ | ------------------------------------------- |
| Tables created by migration        | PASS   | Flyway v4                                   |
| create_attempt → submitted_at NULL | PASS   | repository + ExamApiTest path               |
| save_answer insert/replace         | PASS   | upsert semantics                            |
| submit sets submitted_at and score | PASS   |                                             |
| get attempt with answers           | PASS   | used by submit/review                       |
| Repository/unit tests pass         | PASS   | covered via ExamApiTest against PostgreSQL  |
| Existing bootstrap still works     | PASS   | Flyway history intact; questions/quizzes OK |

### Test Output

```
Flyway: version "4 - create exam attempts"
./mvnw test → BUILD SUCCESS (ExamApiTest exercises repository)
```

---

## 5. Known Limitations

* No dedicated `*ExamRepository*` unit class name; behavior verified through API tests.
* No HTTP layer yet (o03/t02).

---

## 6. Next Suggested Task

**Next task:** `o03/t02-implement-exam-api`
**Context:** Expose `/api/exams/attempts` create, answer, submit endpoints.
