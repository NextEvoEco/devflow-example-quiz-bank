# Evidence: Build Available Exams Page

**ID:** o03-e03-build-available-exams-page
**Task Ref:** `.devflow/tasks/o03/t03-build-available-exams-page.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~40 min
**Status:** completed

---

## 1. Summary

Added the Online Exam section to the frontend. Enabled the previously-disabled
Online Exam sidebar item and built the Available Exams (`examList`) page: it
fetches saved quizzes from the existing `GET /api/quizzes` (V2, no new exam API
calls) and renders each as an exam card (name, question-count badge, full-width
"Start Exam" button), with an empty state when no quizzes exist. Start Exam
stores the selected quiz id in `window.currentExamQuizId` and navigates to an
`examTaking` placeholder page (the real in-exam question view is o03/t04). Built
on the shared navigation controller with a new `exam-list.js` module, leaving the
Question Bank and Quiz Builder pages/navigation untouched. Verified with 125
passing tests and a real-browser session.

---

## 2. Files Changed

| File                           | Change Type | Description                                                                                                                                                                          |
| ------------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `frontend/index.html`          | modified    | Enabled Online Exam nav (`data-page="examList"`); added `examList` page (exam card grid + empty state) and `examTaking` placeholder page; loads `exam-list.js`                       |
| `frontend/js/app.js`           | modified    | Extended the nav controller's `NAV_GROUP` / `TOP_BAR_TITLES` maps with exam pages (examList/examTaking/examResults) — additive, QB/Quiz logic unchanged                              |
| `frontend/js/exam-list.js`     | created     | Available Exams module: load/render exam cards from `GET /api/quizzes`, Start Exam → store `currentExamQuizId` + navigate; registers `examList` + `examTaking` (placeholder) loaders |
| `frontend/css/style.css`       | modified    | `.exam-start-btn` full-width Start Exam button                                                                                                                                       |
| `tests/test_exam_list_page.py` | created     | 5 tests: nav active, page markup, JS wiring (+ no `/api/exams` call), QB/Quiz nav intact, API-driven list                                                                            |
| `tests/test_v1_release.py`     | modified    | Scope guard: examList/examTaking now in-scope (o03/t03); assert only `page-examResults` absent                                                                                       |
| `tests/test_o02_release.py`    | modified    | Same scope-guard relaxation                                                                                                                                                          |
| `tests/test_quiz_list_page.py` | modified    | Dropped the stale "Online Exam is a disabled placeholder" assertion (now enabled)                                                                                                    |

---

## 3. Behavior Added

* Clicking Online Exam activates the Available Exams page (top bar "Available Exams").
* Each saved quiz renders as an exam card: name + `N questions` badge + full-width
  Start Exam. (Quizzes have no description field in V2, so none is shown.)
* Start Exam stores `window.currentExamQuizId` and navigates to the `examTaking`
  placeholder, which names the quiz and question count (proving the id was carried).
* An empty state ("No exams available") shows when there are no quizzes.
* No calls to the new `/api/exams` endpoints (per task boundary).

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                          | Result | Notes                                                                       |
| ---------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------- |
| "Online Exam" appears in the sidebar and activates the Available Exams view        | PASS   | nav enabled; click → examList shown, top bar "Available Exams"              |
| Available Exams fetches quizzes from `GET /api/quizzes` and renders a card each    | PASS   | 2 seeded quizzes → 2 cards                                                  |
| Each card shows title, description, question count, and a Start Exam button        | PASS   | name + `N questions` badge + Start Exam (no description — not stored in V2) |
| Start Exam transitions to the in-exam view placeholder (or stores `currentQuizId`) | PASS   | `window.currentExamQuizId=2`; navigated to examTaking naming the quiz       |
| Empty state message is shown when no quizzes exist                                 | PASS   | deleted quizzes → "No exams available"                                      |
| Question Bank and Quiz Builder navigation remain fully functional                  | PASS   | navigated back: QB 4 rows, Quiz Builder 2 cards, correct titles             |

### Test Output

```
$ python -m pytest -q
125 passed in 3.34s

# Live browser verification (4 questions + 2 quizzes seeded):
- sidebar: all three nav items enabled (Question Bank, Quiz Builder, Online Exam)
- click Online Exam -> examList, top bar "Available Exams", cards "Math Exam / 3 questions", "Science Exam / 4 questions"
- Start Exam on "Science Exam" -> examTaking, currentExamQuizId=2, target "Starting \"Science Exam\" (#2) - 4 questions", Online Exam stays active
- back link -> examList; nav to Question Bank (4 rows) and Quiz Builder (2 cards) -> intact
- delete all quizzes -> "No exams available" empty state
- console errors: none
```

---

## 5. Known Limitations

* `examTaking` is a placeholder; the real one-question-at-a-time view with
  navigation and answer selection is o03/t04.
* Exam cards show no description because quizzes don't persist one (V2 scope).
* The task references `frontend/css/app.css`; the actual stylesheet is
  `frontend/css/style.css` (used consistently since o01). No rename made.

---

## 6. Next Suggested Task

**Next task:** `o03/t04-build-exam-question-view`
**Context:** The seam is ready: Start Exam sets `window.currentExamQuizId` and
navigates `examTaking` with `{quizId}`; `exam-list.js` registers a placeholder
`examTaking` loader that t04 should replace with the real question view (own
module, e.g. `frontend/js/exam-taking.js`). t04 should: create an attempt via
`POST /api/exams/attempts {quiz_id}`, fetch quiz questions (see the o03/t02
limitation — `GET /api/quizzes/<id>` returns `correct`, so the exam UI must not
display it), show one question at a time with free prev/next navigation, save
each selection via `PUT /api/exams/attempts/{id}/answers/{qid}`, and Submit via
`POST .../submit` then route to `examResults` (o03/t05). Per `ui-spec.md`:
progress bar, option buttons with single-select, Previous dimmed on Q1,
Next→Submit on the last question. See `.devflow/memory.md` for the nav controller.
