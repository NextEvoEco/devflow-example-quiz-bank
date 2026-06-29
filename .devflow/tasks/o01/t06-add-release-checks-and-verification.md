# Task: Add Release Checks And Verification

**ID:** o01/t06-add-release-checks-and-verification
**File:** `.devflow/tasks/o01/t06-add-release-checks-and-verification.md`
**Objective Ref:** `.devflow/objective/o01-question-bank-v1.md`
**Depends On:** o01/t05-build-question-editor-and-delete-flows
**Complexity:** M
**Estimated Duration:** 1 hr
**Status:** verified

---

## 1. Purpose

> What does this task accomplish within the objective?

This task brings Question Bank V1 to a releaseable baseline by tightening automated checks, validating local startup behavior, and ensuring the V1 scope is documented and verifiable.

---

## 2. Boundary

### In Scope

* Add or complete the basic automated test coverage required for V1.
* Verify local startup, SQLite behavior, and Question Bank CRUD/search flows.
* Document or update the local run/test instructions required for a releaseable V1 demonstration.
* Confirm out-of-scope features remain excluded.

### Out of Scope

* New product features.
* V2 or V3 functionality.
* Enterprise-grade CI/CD or deployment automation.

---

## 3. Must / Must Not

### Must

* Ensure the V1 app can be started locally and demonstrated.
* Ensure automated checks exist for the confirmed V1 baseline.
* Keep the final verification aligned with the objective success criteria.

### Must Not

* Expand scope under the cover of "polish."
* Leave required startup or verification steps undocumented.

---

## 4. Inputs

| Artifact | Source |
| --- | --- |
| Objective definition | `.devflow/objective/o01-question-bank-v1.md` |
| Completed Question Bank implementation | `o01/t01` through `o01/t05` |
| Existing tests and startup flow | repository codebase |

---

## 5. Outputs

| Artifact | Path |
| --- | --- |
| Final V1 automated tests or verification updates | `tests/` |
| Local startup / test instructions updates | `README.md` or `docs/` as needed |
| Release-readiness fixes within V1 scope | repository codebase |

---

## 6. Acceptance Criteria

> These criteria must all pass before the task is marked complete.

* [x] The application can be started locally and demonstrated as a V1 Question Bank web app.
* [x] Automated tests cover the basic V1 backend and/or integration baseline.
* [x] Local run and verification steps are documented clearly enough for a fresh user or AI session.
* [x] The final V1 build still excludes Quiz Builder and Online Exam functionality.

---

## 7. Test Plan

```text
1. Run the documented automated tests.
2. Start the application from a clean local state.
3. Verify list, search, add, edit, and delete flows manually in the browser.
4. Verify SQLite persistence works as intended for V1.
5. Review the codebase and UI to confirm out-of-scope features remain unimplemented.
```

---

## 8. Notes

This is the release-readiness task for the V1 scope, not a catch-all feature expansion task.
