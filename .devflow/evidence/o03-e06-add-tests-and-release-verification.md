# Evidence: Add Tests and Release Verification

**ID:** o03-e06-add-tests-and-release-verification
**Task Ref:** `.devflow/tasks/o03/t06-add-tests-and-release-verification.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Status:** completed

---

## 1. Summary

Completed the V3 release verification layer by adding dedicated Online Exam release tests, documenting the V3 manual verification flow, updating the repository README to reflect the shipped version, and re-running the full regression suite plus local startup smoke checks.

---

## 2. Files Changed

| File                                    | Change Type | Description                                                                                                         |
| --------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------- |
| `tests/test_v3_release_verification.py` | created     | Added end-to-end V3 release checks for full exam flow, abandoned attempt persistence, and double-submit protection. |
| `docs/v3-verification.md`               | created     | Added V3 manual verification and release-readiness checklist.                                                       |
| `README.md`                             | modified    | Updated project status to V3 and linked the V3 verification guide.                                                  |
| `.devflow/status.md`                    | modified    | Advanced runtime state to `o03/t06`, then marked it verified and noted V3 completion.                               |

---

## 3. Verification Added

* Full V3 release flow test now covers:
  * homepage shell includes Online Exam
  * quiz creation for an exam
  * attempt creation
  * answer saving
  * submission scoring
  * double-submit returning 409
* Abandoned attempt test now verifies that an unsubmitted attempt remains unscored with `submitted_at = NULL`.
* Added a dedicated V3 manual verification guide for local release checks.
* Updated README so the repository status matches the shipped V3 Online Exam scope.

---

## 4. Acceptance Criteria Check

| Criterion                                                                               | Result | Notes                                                        |
| --------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------ |
| `pytest tests/ -v` passes with zero failures                                            | PASS   | Full suite passed after adding V3 release checks.            |
| Full exam flow test covers create attempt, save answers, submit, and score verification | PASS   | Covered by `test_v3_online_exam_release_flow`.               |
| Abandoned attempt remains unsubmitted with `submitted_at = NULL`                        | PASS   | Covered by `test_v3_abandoned_attempt_remains_unsubmitted`.  |
| Double-submit returns 409                                                               | PASS   | Verified in the V3 release flow test.                        |
| Manual smoke steps for Online Exam are documented                                       | PASS   | Documented in `docs/v3-verification.md`.                     |
| Existing V1 and V2 tests remain green                                                   | PASS   | Full regression suite passed with all previous tests intact. |

---

## 5. Verification

```text
py -m pytest tests/test_v3_release_verification.py -v
2 passed in 0.17s

py -m pytest tests -v
60 passed in 1.60s

node --check frontend/app.js
pass

Local startup smoke
HOME=200
HEALTH=200
```

---

## 6. Notes

* The task note referenced `docs/v1-verification.md`, but the live repository already uses release walkthrough files such as `docs/v1-question-bank-release.md` and `docs/v2-quiz-builder-release.md`, so the V3 guide was added as `docs/v3-verification.md` for consistency.
* Frontend end-to-end interaction is covered indirectly through release tests plus startup and shell verification; no separate browser automation tool was available in the active toolset for this run.

---

## 7. Outcome

V3 Online Exam is now release-verified across automated checks, local startup smoke, and documented manual verification steps.
