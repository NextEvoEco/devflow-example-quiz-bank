# Evidence: Integration Testing And Release Verification (V2)

**ID:** o02-e06-integration-testing
**Task Ref:** `.devflow/tasks/o02/t06-integration-testing.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~40 min
**Status:** completed

---

## 1. Summary

Verified Quiz Builder V2 end-to-end and confirmed no Question Bank regression,
bringing the V2 iteration to a releaseable state. Added a V2 integration/release
test suite that ties the full quiz lifecycle together (create → list → get →
update/reorder → delete), asserts the minimum-3-questions rule on both create and
update, exercises Question Bank CRUD + search as a regression guard, verifies the
question-delete → quiz cascade, and guards the Online Exam (V3) scope boundary.
Ran the full suite from a clean state (98 passing) and performed a complete
browser walkthrough: create → reorder → preview → min-3 error → save → edit →
delete, plus a Question Bank add/search/edit/delete regression pass. Extended
`docs/verification.md` with a V2 checklist and marked V2 complete in the README.

---

## 2. Files Changed

| File                        | Change Type | Description                                                                                                                                                              |
| --------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tests/test_o02_release.py` | created     | V2 integration/release checks: full lifecycle, min-3 (create + update), reorder persistence, QB CRUD+search regression, question-delete cascade, Online Exam scope guard |
| `docs/verification.md`      | modified    | Added the full V1+V2 test-file table, a Quiz Builder (V2) manual checklist, and an updated V1+V2 scope confirmation                                                      |
| `README.md`                 | modified    | Marked "V2 — Quiz Builder (Complete)"                                                                                                                                    |

---

## 3. Behavior Added

* Automated end-to-end coverage of the quiz lifecycle and the min-3 rule
  (previously covered per-endpoint; now also as a single integrated flow).
* A regression guard asserting Question Bank CRUD + search are unaffected by V2.
* A scope guard failing if `/api/exams` or exam page views appear before V3.
* Documented, reproducible V2 verification steps for a fresh user or AI session.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                       | Result | Notes                                                                       |
| ------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------- |
| `py -m pytest tests/ -v` passes with no failures                                | PASS   | 98 passed from a clean state                                                |
| Quiz API tests cover create, list, get, update, delete, and min-3 rejection     | PASS   | `test_quizzes_api.py` + `test_o02_release.py` (min-3 on create AND update)  |
| Manual walkthrough completed: create → reorder → preview → save → edit → delete | PASS   | Full browser run (see below)                                                |
| Question Bank CRUD and search flows are unaffected                              | PASS   | Browser: list 5, search→1, add→6, delete→5; automated regression test green |
| Evidence artifact written with test results and walkthrough notes               | PASS   | this file                                                                   |

### Test Output

```
$ python -m pytest tests/ -q
..........................................................................  [ 73%]
..........................                                                  [100%]
98 passed in 2.08s

# Browser walkthrough (5 questions seeded):
- New Quiz "V2 Walkthrough": add 3, reorder (move 3rd to top)
- Preview: order == builder order; correct answers marked C/A/B; close
- remove one -> Save -> error "A quiz requires at least 3 questions." (stayed on builder)
- add back to 3 -> Save -> quizList shows "V2 Walkthrough / 3 questions"
- Edit: prefilled name + 3 questions; rename to "...(edited)" + add one -> 4 questions
- Delete -> confirm -> count 0, empty state "No quizzes yet"
- Question Bank regression: list 5 rows; search "planet" -> only "Largest planet?"
  (UI and /api/questions?search=planet agree); add -> 6; delete -> 5
- console errors: none

# Scope check:
- backend/ and backend/routes/ contain no exam modules
- GET /api/exams -> 404 (asserted in tests)
```

---

## 5. Known Limitations

* No performance/load or cross-browser testing (out of scope per the task).
* During the browser walkthrough, one search measurement transiently read a
  pre-debounce state (dispatched `input` event without `bubbles`); re-running the
  search confirmed correct filtering in both the UI and the API — a harness
  timing artifact, not a defect.

---

## 6. Next Suggested Task

**Next task:** `o03/t01-add-exam-attempts-schema` (start of Objective o03 — Online Exam V1)
**Context:** Objectives o01 (Question Bank) and o02 (Quiz Builder) are complete
and release-verified (98 tests). The codebase: Flask app factory
`create_app(db_path)`; versioned SQLite migration at `user_version = 2`
(`questions`, `quizzes`, `quiz_questions`); `/api/questions` + `/api/quizzes`
blueprints; a multi-page frontend with a shared nav controller (see
`.devflow/memory.md`) and an inactive Online Exam sidebar item. V3 should extend
the migration (v3: exam attempts/answers), add an `/api/exams` blueprint and a
repository, and build the `examList` / `examTaking` / `examResults` pages —
reusing `GET /api/quizzes/<id>` (which returns ordered questions with correct
answers) for exam content. Run/verify steps are in `docs/verification.md`.
