# Evidence: Add Release Checks And Verification

**ID:** o01-e06-add-release-checks-and-verification
**Task Ref:** `.devflow/tasks/o01/t06-add-release-checks-and-verification.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Execution Time:** 16:49-16:57 UTC+8, ~8 min
**Status:** completed

---

## 1. Summary

Completed the V1 release-readiness pass by adding a dedicated release verification test, documenting a fresh-user startup and manual verification guide, and re-running automated plus live startup checks against a clean SQLite database. The final V1 state remains limited to Question Bank functionality while preserving visible but disabled future-version navigation labels.

---

## 2. Files Changed

| File                                    | Change Type | Description                                                                                                              |
| --------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| `tests/test_v1_release_verification.py` | created     | Added release-focused verification for persistence across app instances and V1 scope boundaries on the homepage.         |
| `docs/v1-question-bank-release.md`      | created     | Added V1 startup, automated-test, manual verification, and data reset instructions.                                      |
| `README.md`                             | modified    | Linked the dedicated V1 release verification guide from the startup section.                                             |
| `.devflow/status.md`                    | modified    | Moved runtime state to `o01/t06`, then marked the release task verified and recorded objective-complete resume guidance. |

---

## 3. Behavior Added

* The repository now has a dedicated V1 release verification test that checks startup/persistence behavior and confirms out-of-scope product areas remain disabled in the homepage shell.
* A fresh user or fresh AI session can now follow a single release guide to install dependencies, start the app, run tests, reset demo data, and manually verify Question Bank flows.
* The documented release steps were re-validated against a clean temporary SQLite database.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                                      | Result | Notes                                                                                                                              |
| ---------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| The application can be started locally and demonstrated as a V1 Question Bank web app.         | PASS   | Verified with a clean startup smoke check against a temporary SQLite database.                                                     |
| Automated tests cover the basic V1 backend and/or integration baseline.                        | PASS   | Full test suite now includes dedicated V1 release verification coverage.                                                           |
| Local run and verification steps are documented clearly enough for a fresh user or AI session. | PASS   | Added `docs/v1-question-bank-release.md` and linked it from `README.md`.                                                           |
| The final V1 build still excludes Quiz Builder and Online Exam functionality.                  | PASS   | Release verification test confirms those items remain visible-but-disabled in the homepage shell, with no implemented flows in V1. |

### Test Output

```text
> py -m pytest
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 28 items

tests\test_bootstrap.py ...                                              [ 10%]
tests\test_question_api.py .........                                     [ 42%]
tests\test_question_bank_page.py .                                       [ 46%]
tests\test_question_editor_page.py .                                     [ 50%]
tests\test_questions.py ............                                     [ 92%]
tests\test_v1_release_verification.py ..                                 [100%]

============================= 28 passed in 0.33s ==============================

> clean release smoke
GET / -> 200
GET /health -> 200
GET /api/questions -> {"items":[]}
POST /api/questions -> 201
GET /api/questions?q=Taiwan -> seeded match returned
```

---

## 5. Known Limitations

* I validated release behavior through automated tests and clean HTTP smoke checks, but did not run full browser automation for visual click-by-click regression.
* V1 intentionally stops at Question Bank; later objectives will add working Quiz Builder and Online Exam behavior.

---

## 6. Next Suggested Task

**Next task:** `o02/t01-quiz-db-schema`
**Context:** Objective o01 is now release-ready and documented. The next objective can build Quiz Builder foundations without reworking the V1 Question Bank baseline.
