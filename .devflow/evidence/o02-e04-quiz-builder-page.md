# Evidence: Quiz Builder Page

**ID:** o02-e04-quiz-builder-page
**Task Ref:** `.devflow/tasks/o02/t04-quiz-builder-page.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~70 min
**Status:** completed

---

## 1. Summary

Replaced the t03 `quizCreate` placeholder with the real Quiz Builder. Users can
name a quiz, browse the Question Bank (with a live search), add questions into a
Selected panel, reorder them with up/down controls, remove them, and save
(create via `POST`, edit via `PUT`). A client-side guard blocks saving with
fewer than 3 questions (the API enforces the same rule as a backstop). Edit mode
pre-populates the name and question order from `GET /api/quizzes/<id>`. The
Preview button calls a `window.openQuizPreview(draft)` hook that t05 will
provide. Duplicate selection is impossible: the Add panel only lists
not-yet-selected questions. The Question Bank module was not touched. Verified
with 87 passing tests and a full real-browser session (create → reorder →
min-3 error → save → edit prefill → preview hook → search).

---

## 2. Files Changed

| File                              | Change Type | Description                                                                                                                                                          |
| --------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/index.html`             | modified    | Replaced `#page-quizCreate` placeholder with the builder layout (name card, Selected panel, Add panel + search, footer Preview/Cancel/Save); loads `quiz-builder.js` |
| `frontend/js/quiz-builder.js`     | created     | Builder module: load/prefill, render selected+available, add/remove/reorder, min-3 + name validation, save POST/PUT, preview hook; registers the `quizCreate` loader |
| `frontend/js/quiz-list.js`        | modified    | Removed the temporary quizCreate placeholder loader/refs (ownership moved to the builder module); kept `openBuilder` navigation                                      |
| `frontend/css/style.css`          | modified    | Builder page (720px), cards, rows, reorder/remove buttons, add button, footer                                                                                        |
| `tests/test_quiz_builder_page.py` | created     | 4 tests: markup, JS wiring, ownership moved, end-to-end API lifecycle                                                                                                |

---

## 3. Behavior Added

* Quiz name input (required to save).
* Add Questions panel lists every bank question not already selected, filtered
  live by a search box; each row shows question text + difficulty badge + Add.
* Selected Questions panel shows count badge and ordered rows with ↑/↓ (disabled
  at the ends), a remove ×, and difficulty badge; "No questions selected" when empty.
* Add moves a question into Selected; Remove returns it to the available pool; a
  selected question never reappears in the Add panel (no duplicates).
* Save validates name + min-3 client-side, sends `{name, questionIds}` in panel
  order, and on success returns to the Quiz List; validation/API errors show inline.
* Preview button invokes `window.openQuizPreview(draft)` if present (t05), else logs.
* Edit mode prefills name and ordered questions from the API.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                           | Result | Notes                                                           |
| ------------------------------------------------------------------- | ------ | --------------------------------------------------------------- |
| User can enter a quiz name                                          | PASS   | name input; save requires it                                    |
| Question browser shows all questions from the Question Bank         | PASS   | 5 seeded questions listed                                       |
| User can add a question to the selected panel                       | PASS   | Add → moved, count updates                                      |
| A question already selected cannot be added again                   | PASS   | Add panel excludes selected (+guard in `addSelected`)           |
| User can remove a question from the selected panel                  | PASS   | × → returns to available                                        |
| User can reorder selected questions using up/down controls          | PASS   | ↑ moved a row; end buttons disabled                             |
| Saving with fewer than 3 questions is blocked with a visible error  | PASS   | "A quiz requires at least 3 questions."; stayed on builder      |
| Saving with 3+ succeeds and returns to the Quiz List                | PASS   | saved → quizList shows "Science Basics / 3 questions"           |
| Edit mode loads the existing quiz name and question order correctly | PASS   | name + 3 questions in saved order; 2 remaining available        |
| "Preview" button is present and functional (links to t05)           | PASS   | invokes `openQuizPreview(draft)` with name + selected questions |

### Test Output

```
$ python -m pytest -q
87 passed in 1.78s

# Live browser verification (5 questions seeded):
- New Quiz: 5 available, 0 selected
- add x3 -> 3 selected, 2 available, first ↑ disabled
- reorder: ↑ on 3rd row -> order changes as expected
- remove one -> 2 selected; Save -> error "A quiz requires at least 3 questions." (stays on builder)
- add back -> 3; Save -> navigates to quizList; card "Science Basics / 3 questions"
- Edit that card -> "Edit Quiz", name + 3 questions in saved order prefilled
- Preview -> openQuizPreview(draft) received {name, 3 questions}
- Add search "planet" -> only "Largest planet?" listed
- console errors: none
```

---

## 5. Known Limitations

* No description field: `ui-spec.md` shows an optional quiz description, but the
  V2 schema/objective exclude it (see o02-e01) and the task lists only a name
  input — so it is intentionally omitted.
* Reorder is up/down only (drag-and-drop not required per task notes).
* Preview is a hook stub until t05 provides `window.openQuizPreview`.

---

## 6. Next Suggested Task

**Next task:** `o02/t05-quiz-preview`
**Context:** The builder already calls `window.openQuizPreview(draft)` where
`draft = { name, questions: [full question objects in order] }`; t05 should
define that global (e.g. a modal) to show the full quiz — question text, all
options, and the correct answer — before saving. `GET /api/quizzes/<id>` also
returns the same `questions` shape if a saved-quiz preview is wanted. The nav
controller, card grid, and builder stay unchanged; t05 only adds the preview UI
and the hook implementation.
