# Task: Integration Testing And Release Verification

**ID:** o02/t06-integration-testing
**File:** `.devflow/tasks/o02/t06-integration-testing.md`
**Objective Ref:** `.devflow/objective/o02-quiz-builder-v1.md`
**Depends On:** o02/t05-quiz-preview
**Complexity:** M
**Estimated Duration:** 1 hr
**Status:** complete

---

## 1. Purpose

Verify that the full Quiz Builder V1 feature works end-to-end and that no existing Question Bank behavior has regressed. After this task, the Quiz Builder iteration is releaseable.

---

## 2. Boundary

### In Scope

- Automated tests for the Quiz API (create, read, update, delete, validation)
- Regression run of all existing Question Bank tests
- Manual end-to-end walkthrough of the core Quiz Builder flow
- Evidence artifact documenting the verification outcome

### Out of Scope

- Performance or load testing
- Browser compatibility testing beyond the development browser
- Online Exam functionality

---

## 3. Must / Must Not

### Must

- All automated tests must pass (new + existing)
- The minimum-3-questions validation must be covered by an automated test
- The manual walkthrough must cover: create quiz, reorder, preview, save, edit, delete
- Evidence must be written to `.devflow/evidence/`

### Must Not

- Mark the objective complete without a passing test run
- Skip the regression check on Question Bank tests

---

## 4. Inputs

| Artifact                | Source               |
| ----------------------- | -------------------- |
| Quiz Preview page (t05) | o02/t05-quiz-preview |
| All prior o02 tasks     | o02/t01–t05          |
| Existing test suite     | `tests/`             |

---

## 5. Outputs

| Artifact           | Path                                               |
| ------------------ | -------------------------------------------------- |
| New quiz API tests | `tests/`                                           |
| Evidence artifact  | `.devflow/evidence/o02-e06-integration-testing.md` |

---

## 6. Acceptance Criteria

- [x] `py -m pytest tests/ -v` passes with no failures
- [x] Quiz API tests cover: create, list, get, update, delete, and the min-3 validation rejection
- [x] Manual walkthrough completed: create → reorder → preview → save → edit → delete
- [x] Question Bank CRUD and search flows are unaffected
- [x] Evidence artifact written with test results and walkthrough notes

---

## 7. Test Plan

```
py -m pytest tests/ -v
py -m backend
# manual walkthrough in browser:
# 1. create quiz with 3 questions, verify save succeeds
# 2. attempt save with 2 questions, verify error shown
# 3. reorder questions, preview, confirm order matches
# 4. edit quiz: rename, add/remove question, save
# 5. delete quiz, verify removed from list
# 6. verify Question Bank list, add, edit, delete still work
```

---

## 8. Notes

Write the evidence artifact during or immediately after verification. Include the test output summary and any noteworthy observations about edge cases.
