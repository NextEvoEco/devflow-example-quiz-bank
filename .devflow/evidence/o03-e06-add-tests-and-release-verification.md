# Evidence: Add Tests and Release Verification (V3)

**ID:** o03-e06-add-tests-and-release-verification
**Task Ref:** `.devflow/tasks/o03/t06-add-tests-and-release-verification.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~35 min
**Status:** completed

---

## 1. Summary

Verified the complete Online Exam V3 flow end-to-end and confirmed V1/V2 have no
regression, bringing V3 to a releaseable state and completing the whole
three-version roadmap. Added a V3 integration/release test suite covering the
full exam flow (create → answer → submit → score), the unanswered-counts-as-wrong
and double-submit (409) rules, the abandoned-attempt-stays-unscored rule (checked
against the database), the no-correct-answers-before-submit invariant, and a
V1/V2 regression pass, plus a check that all six app views are present. Wrote
`docs/v3-verification.md`, linked it from `docs/verification.md` and the README,
and marked V3 complete in the README. Ran the full suite from a clean state (143
passing) and performed a full browser smoke of the exam flow.

---

## 2. Files Changed

| File                       | Change Type | Description                                                                                                                                                           |
| -------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tests/test_v3_release.py` | created     | V3 release checks: full flow + scoring, unanswered, abandonment (DB), double-submit 409, no correct-leak, available-exams source, V1/V2 regression, all-views-present |
| `docs/v3-verification.md`  | created     | V3 test-file table + Online Exam manual checklist + scope confirmation                                                                                                |
| `docs/verification.md`     | modified    | Retitled to cover V1+V2, links to `v3-verification.md`, updated scope section to all three versions complete                                                          |
| `README.md`                | modified    | Marked "V3 — Online Exam (Complete)"; linked both verification docs                                                                                                   |

---

## 3. Behavior Added

* Automated end-to-end coverage of the exam flow and its scoring/edge rules as a
  single integrated suite (complementing the per-endpoint tests in `test_exam_api.py`).
* A database-level assertion that an abandoned attempt (never submitted) stays
  pending (`submitted_at`/`score`/`total` NULL).
* A guard that the exam API never returns `correct` before submission.
* A V1/V2 regression pass and an all-six-views-present check.
* Documented, reproducible V3 verification steps for a fresh user or AI session.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                               | Result | Notes                                                                             |
| ----------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------- |
| `pytest tests/ -v` passes with zero failures                            | PASS   | 143 passed from a clean state                                                     |
| Full exam flow test: create → save → submit → correct score             | PASS   | `test_full_exam_flow_scores_correctly` (2/3, 67%)                                 |
| Abandoned attempt has `submitted_at = NULL`                             | PASS   | `test_abandoned_attempt_stays_unscored` (via `EXAM_REPOSITORY`)                   |
| Double-submit returns 409                                               | PASS   | `test_double_submit_returns_409`                                                  |
| Manual smoke: Available Exams lists quizzes; full flow works in browser | PASS   | list → start → answer all → submit → 100% green ring → retry → back; V1/V2 intact |
| `docs/v3-verification.md` documents V3 manual steps                     | PASS   | created + linked                                                                  |

### Test Output

```
$ python -m pytest tests/ -q
143 passed in 3.88s

# Browser smoke (3-question "Smoke Exam", correct B/C/A):
- Online Exam -> Available Exams lists "Smoke Exam"
- Start Exam -> Q1 loads; answer all 3 correct; last button = "Submit"
- Submit -> Results: 100%, green ring, 3 correct, 3 Answer Review rows
- Retry Quiz -> fresh examTaking (0 selections); Exit -> examList
- regression: Question Bank 3 rows, Quiz Builder 1 card
```

---

## 5. Known Limitations

* No load/performance or cross-browser testing (out of scope per the task).
* Browser verification is driven via the preview tool. When seeding a running dev
  server, seed through the app's own API — a separate process touching
  `data/quiz_bank.db` while the reloader server holds it causes transient
  `no such table` 500s on the first load (an environment race, not an app bug;
  all 143 tests pass against isolated per-test databases).

---

## 6. Next Suggested Task

**Roadmap complete.** Objectives o01 (Question Bank), o02 (Quiz Builder), and o03
(Online Exam) are all implemented and release-verified — 143 passing tests plus
browser/curl verification, with per-task evidence under `.devflow/evidence/`. The
app is a runnable local Flask + SQLite + plain HTML/CSS/JS Quiz Bank started with
`py -m backend`; tests run with `py -m pytest`; verification steps are in
`docs/verification.md` (V1+V2) and `docs/v3-verification.md` (V3). No further
tasks are queued — await a new intent/objective from the user.
