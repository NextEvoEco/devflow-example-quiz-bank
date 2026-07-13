# Evidence: Add Tests And Release Verification

**ID:** o03-e06-add-tests-and-release-verification
**Task Ref:** `.devflow/tasks/o03/t06-add-tests-and-release-verification.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** ~15:30-15:36 UTC+8 (implementation pass); smoke reconfirmed 2026-07-12
**Status:** completed

---

## 1. Summary

Completed Online Exam release verification: full `./mvnw test` green including
`ExamApiTest` (create → answers → submit, abandoned attempt, double-submit 409),
frontend test/build green, black-box HTTP smoke scoring 3/3, and
`docs/v3-verification.md` documenting manual V3 checks. SPA loads with all three
sidebar sections.

---

## 2. Files Changed

| File                                                              | Change Type | Description                  |
| ----------------------------------------------------------------- | ----------- | ---------------------------- |
| `backend/src/test/java/com/quizbank/web/ExamApiTest.java`         | created     | exam flow + error cases      |
| `docs/v3-verification.md`                                         | created     | manual V3 verification notes |
| `.devflow/evidence/o03-e06-add-tests-and-release-verification.md` | created     | this evidence                |

---

## 3. Behavior Added

* Automated regression for the exam API happy path and conflict/not-found cases.
* Documented release smoke path for V3 Online Exam.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                     | Result | Notes                        |
| --------------------------------------------- | ------ | ---------------------------- |
| `./mvnw test` zero failures                   | PASS   |                              |
| Full exam flow test correct score             | PASS   | ExamApiTest + HTTP smoke 3/3 |
| Abandoned attempt submitted_at NULL           | PASS   | ExamApiTest                  |
| Double-submit → 409                           | PASS   | ExamApiTest                  |
| Manual/API smoke Available Exams + end-to-end | PASS   | HTTP smoke + SPA nav         |
| `docs/v3-verification.md` present             | PASS   |                              |

### Test Output

```
./mvnw test → BUILD SUCCESS
npm test → passed
npm run build → passed
GET /api/health → ok
POST quiz + attempt + answers + submit → score 3/3 percentage 100
GET / → 200 Quiz Bank SPA (Quiz + Exam in bundle)
```

---

## 5. Known Limitations

* Seed import (`scripts/import_seed_from_sqlite.py`) is optional and separate from V3 AC.

---

## 6. Next Suggested Task

**Next task:** `(none — o01/o02/o03 complete)`
**Context:** Optional follow-up: keep or remove `data/quiz_bank.db` after seed import per memory.md.
