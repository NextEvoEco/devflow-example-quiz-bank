# Evidence: Add Release Checks And Verification

**ID:** o01-e06-add-release-checks-and-verification
**Task Ref:** `.devflow/tasks/o01/t06-add-release-checks-and-verification.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-11
**Execution Time:** ~18:45-18:50 UTC+8, ~5 min
**Status:** completed

---

## 1. Summary

Added V1 release tests and `docs/v1-verification.md`. Confirmed Question Bank CRUD works locally; Quiz Builder / Online Exam routes and sidebar entries remain absent for V1.

---

## 2. Files Changed

| File                       | Change Type | Description                        |
| -------------------------- | ----------- | ---------------------------------- |
| `tests/test_v1_release.py` | created     | V1 release + scope exclusion tests |
| `docs/v1-verification.md`  | created     | Startup and smoke checklist        |

---

## 3. Behavior Added

* Documented V1 verification steps
* Automated release flow covering health, CRUD, and out-of-scope route absence

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                      | Result | Notes                   |
| ------------------------------ | ------ | ----------------------- |
| Local demo as V1 Question Bank | PASS   | Running app + browser   |
| Automated V1 baseline          | PASS   | 13 pytest tests         |
| Documented run/verify steps    | PASS   | docs/v1-verification.md |
| Quiz/Exam excluded             | PASS   | No nav entries; API 404 |

### Test Output

```
py -m pytest tests -v
13 passed
```

---

## 5. Known Limitations

* `test_v1_excludes_quiz_and_exam_routes` must be updated when o02/o03 APIs land

---

## 6. Next Suggested Task

**Next task:** `o02/t01-quiz-db-schema`
**Context:** Begin Quiz Builder; extend SCHEMA_VERSION migrations.
