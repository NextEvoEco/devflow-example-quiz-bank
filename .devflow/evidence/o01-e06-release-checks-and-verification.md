# Evidence: Add Release Checks And Verification

**ID:** o01-e06-release-checks-and-verification
**Task Ref:** `.devflow/tasks/o01/t06-add-release-checks-and-verification.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~35 min
**Status:** completed

---

## 1. Summary

Brought Question Bank V1 to a releaseable baseline. Added a release-verification
test suite that ties the objective success criteria together (startup, full
CRUD + search lifecycle, validation, difficulty default, empty-on-first-run) and
guards the V1 scope boundary (no Quiz Builder / Online Exam endpoints or views).
Wrote a local run & verification guide in `docs/verification.md` and linked it
from `README.md`, and updated the README status to mark V1 complete. Verified
end-to-end: 52 passing tests from a clean state, plus a clean-start browser
session confirming the empty state, add + persistence across a restart, correct
rendering, and `404` for out-of-scope endpoints.

---

## 2. Files Changed

| File                       | Change Type | Description                                                                                                                                                        |
| -------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tests/test_v1_release.py` | created     | Release checks: startup, restart persistence, full CRUD+search lifecycle, validation + difficulty default, empty-on-first-run, out-of-scope endpoints/views absent |
| `docs/verification.md`     | created     | Local run + automated test + manual verification checklist + V1 scope confirmation                                                                                 |
| `README.md`                | modified    | Linked `docs/verification.md`; changed V1 status from "In Progress" to "Complete"                                                                                  |

---

## 3. Behavior Added

* An automated guard that fails if Quiz Builder (`/api/quizzes`) or Online Exam
  (`/api/exams`) endpoints or views are ever added under the V1 scope.
* An automated check that SQLite data persists across an app restart (fresh app
  instance on the same database file).
* A single end-to-end lifecycle test mirroring the objective success criteria.
* Documented, reproducible run/verify steps for a fresh user or AI session.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                 | Result | Notes                                                                                                    |
| ------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------- |
| App can be started locally and demonstrated as a V1 Question Bank web app | PASS   | `py -m backend` served the app; browser showed empty state → add → persisted question                    |
| Automated tests cover the basic V1 backend and/or integration baseline    | PASS   | 52 tests across bootstrap, repository, API, page, flows, and release suites                              |
| Local run and verification steps documented clearly for a fresh user/AI   | PASS   | `docs/verification.md` + README link                                                                     |
| Final V1 build still excludes Quiz Builder and Online Exam                | PASS   | `/api/quizzes` and `/api/exams` return 404; no quiz/exam backend modules or page views; guarded by tests |

### Test Output

```
$ python -m pytest -q
....................................................                     [100%]
52 passed in 0.75s

# Clean-state browser verification (fresh DB, py -m backend):
- first load: empty state "No questions yet", count 0
- add via UI: POST /api/questions -> 201; question persisted (correct=C, difficulty=Hard)
- reload page: question renders in table, count 1
- out-of-scope: GET /api/quizzes -> 404, GET /api/exams -> 404
- console errors: none

# Scope check:
- backend/ and backend/routes/ contain no quiz/exam modules
```

---

## 5. Known Limitations

* No CI pipeline — running `py -m pytest` is manual, which matches the V1
  "lightweight local app" constraint (CI/CD is explicitly out of scope).
* Manual browser verification is driven via the preview tool / by hand; there is
  no in-repo headless JS test runner (kept aligned with the pytest-only setup).

---

## 6. Next Suggested Task

**Next task:** `o02/t01-quiz-db-schema` (start of Objective o02 — Quiz Builder V1)
**Context:** Objective o01 (Question Bank V1) is complete and release-verified.
The codebase is a clean vertical slice: Flask app factory (`create_app(db_path)`),
`QuestionRepository` over a versioned SQLite migration (`PRAGMA user_version`,
currently v1 = `questions`), `/api/questions` blueprint, and a plain HTML/CSS/JS
frontend shell whose sidebar already shows inactive Quiz Builder / Online Exam
nav items. V2 should extend the migration (add `quizzes` / `quiz_questions`) and
add a `/api/quizzes` blueprint and the `quizList` / `quizCreate` views without
disturbing the V1 slice. Run/verify steps are in `docs/verification.md`.
