# Task: Add Tests and Release Verification

**ID:** o03/t06-add-tests-and-release-verification
**File:** `.devflow/tasks/o03/t06-add-tests-and-release-verification.md`
**Objective Ref:** `.devflow/objective/o03-online-exam-v1.md`
**Depends On:** o03/t05-build-results-page
**Complexity:** S
**Estimated Duration:** 30 min
**Status:** verified

---

## 1. Purpose

Verify that the complete Online Exam flow meets the V3 success criteria and that existing V1 (Question Bank) and V2 (Quiz Builder) modules are unaffected. Produce a release-ready test baseline for the V3 scope.

---

## 2. Boundary

### In Scope

* Integration tests covering the full exam API flow: create attempt → save answers → submit → verify score.
* Verify that an abandoned attempt (no submit) does not appear as a scored result.
* Verify that submitting an already-submitted attempt returns 409.
* End-to-end smoke test: start app, open Online Exam page, start exam, navigate questions, submit, see results.
* Regression check: all existing V1 and V2 automated tests still pass.
* Update `docs/v1-verification.md` (or create `docs/v3-verification.md`) with the V3 verification steps.

### Out of Scope

* Load testing or performance benchmarking.
* Browser automation beyond what is already established in the test suite.
* New features or bug fixes (those belong in earlier tasks).

---

## 3. Must / Must Not

### Must

* All new tests must pass with `pytest tests/ -v`.
* No existing test may be broken or deleted to make the suite pass.

### Must Not

* Add workarounds or test skips to hide failures.
* Duplicate test coverage that already exists in earlier task tests.

---

## 4. Inputs

| Artifact                       | Source                               |
| ------------------------------ | ------------------------------------ |
| Completed exam API             | `backend/routes/exams.py` (from t02) |
| Completed frontend (all views) | `frontend/` (from t03–t05)           |
| Existing test suite            | `tests/`                             |
| V1 verification doc pattern    | `docs/v1-verification.md`            |

---

## 5. Outputs

| Artifact                      | Path                       |
| ----------------------------- | -------------------------- |
| V3 release integration tests  | `tests/test_v3_release.py` |
| V3 verification documentation | `docs/v3-verification.md`  |

---

## 6. Acceptance Criteria

* [x] `pytest tests/ -v` passes with zero failures.
* [x] Full exam flow test: create attempt → save answers → submit → correct score returned.
* [x] Abandoned attempt test: attempt created but never submitted has `submitted_at = NULL`.
* [x] Double-submit test: second submit on same attempt returns 409.
* [x] Manual smoke: Available Exams page lists quizzes; full exam flow works end-to-end in browser.
* [x] `docs/v3-verification.md` documents the manual verification steps for V3.

---

## 7. Test Plan

```
pytest tests/ -v
# Then manually:
# 1. Start app
# 2. Open Online Exam, verify Available Exams page
# 3. Start exam, answer all questions, submit
# 4. Verify results page
# 5. Retry Quiz, navigate to Question Bank and Quiz Builder — confirm no regressions
```

---

## 8. Notes

Follow the structure of `tests/test_v1_release.py` for the release verification test file.
