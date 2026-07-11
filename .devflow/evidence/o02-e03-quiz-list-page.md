# Evidence: Quiz List Page

**ID:** o02-e03-quiz-list-page
**Task Ref:** `.devflow/tasks/o02/t03-quiz-list-page.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~55 min
**Status:** completed

---

## 1. Summary

Added the Quiz List page and, to support it, introduced a lightweight multi-page
navigation controller (the app was single-page until now). The sidebar Quiz
Builder item is now active and routes to a `quizList` page that renders a
two-column card grid (name + question-count badge) from `GET /api/quizzes`, with
New Quiz / Edit routing to the Quiz Builder page (`quizCreate`) and a
Delete-with-confirmation flow using `DELETE /api/quizzes/<id>`. An empty state
shows when no quizzes exist. The Quiz Builder form itself is out of scope (t04),
so `quizCreate` is a minimal placeholder that proves the New/Edit wiring by
naming the target quiz. The Question Bank page, its nav entry, and its behavior
are untouched. Verified with 83 passing tests and a full real-browser session.

---

## 2. Files Changed

| File                           | Change Type | Description                                                                                                                                                                                  |
| ------------------------------ | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/index.html`          | modified    | Activated Quiz Builder nav (`data-page="quizList"`); added `quizList` page (card grid + empty state), `quizCreate` placeholder page, and Delete Quiz dialog; loads `quiz-list.js`            |
| `frontend/js/app.js`           | modified    | Added a shared navigation controller: `navigate()`, `registerPage()`, sidebar wiring, `pageLoaders` registry, top-bar/active-nav updates. QB logic unchanged; initial page still `questions` |
| `frontend/js/quiz-list.js`     | created     | Quiz List module: load/render cards, New/Edit → builder navigation, delete confirmation; registers `quizList` + `quizCreate` loaders                                                         |
| `frontend/css/style.css`       | modified    | Quiz grid (2-col, 1-col under 720px), quiz card, back link, builder placeholder styles                                                                                                       |
| `tests/test_quiz_list_page.py` | created     | 7 tests: nav active, page/dialog markup, JS wiring, QB-unaffected, API-driven list                                                                                                           |
| `tests/test_v1_release.py`     | modified    | Page-scope guard updated: Quiz Builder views now in-scope (V2); assert Online Exam views (`page-examList`, `page-examTaking`) still absent                                                   |

---

## 3. Behavior Added

* Sidebar navigation now switches between pages via a `currentPage` model; the
  Quiz Builder item activates the `quizList` page and the top bar title updates.
* Quiz List renders one card per quiz (name + `N questions` badge) or an empty
  state ("No quizzes yet").
* New Quiz (header or empty state) and Edit (per card) navigate to the
  `quizCreate` page; the placeholder shows "New Quiz" / "Edit Quiz \"Name\" (#id)".
* Delete opens a confirmation dialog naming the quiz; confirming issues a
  `DELETE` and refreshes the list; Cancel/backdrop/Escape dismiss.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                  | Result | Notes                                                         |
| -------------------------------------------------------------------------- | ------ | ------------------------------------------------------------- |
| Quiz List page loads and displays all saved quizzes                        | PASS   | Browser: 2 seeded quizzes rendered as cards                   |
| Each quiz entry shows its name and question count                          | PASS   | "Algebra Basics / 3 questions", "Full Mix / 4 questions"      |
| "Create Quiz" button navigates to the Quiz Builder page                    | PASS   | New Quiz → `quizCreate`, title "New Quiz"                     |
| "Edit" button navigates to the Quiz Builder with the correct quiz loaded   | PASS   | Edit → `quizCreate`, target "editing \"Algebra Basics\" (#1)" |
| "Delete" button removes the quiz after confirmation and refreshes the list | PASS   | Deleted "Full Mix" → count 2→1; deleted last → empty state    |
| Empty state message is shown when no quizzes exist                         | PASS   | "No quizzes yet" shown after last delete                      |
| Navigation includes a link to the Quiz List page                           | PASS   | Sidebar Quiz Builder item active/enabled                      |
| Question Bank page and navigation are unaffected                           | PASS   | Navigated back: 4 rows, editor present, title "Questions"     |

### Test Output

```
$ python -m pytest -q
83 passed in 1.82s

# Live browser verification (preview server, 4 questions + 2 quizzes seeded):
- initial page = Question Bank (active, 4 questions); Quiz Builder enabled; Online Exam disabled
- click Quiz Builder -> quizList shown, top bar "Quizzes", 2 cards with correct counts
- Edit "Algebra Basics" -> quizCreate, "Edit Quiz", target names quiz #1
- New Quiz -> quizCreate, "New Quiz", create target
- Delete "Full Mix" -> dialog names it -> confirm -> count 2->1
- back to Question Bank -> intact (4 rows, editor present)
- delete last quiz -> empty state "No quizzes yet"
- console errors: none
```

---

## 5. Known Limitations

* `quizCreate` is a placeholder page; the real create/edit form (name input,
  question selection, reordering, min-3 validation, save) is `o02/t04`.
* No quiz search/filter or pagination (out of scope for t03).
* Two delete dialogs now exist (question + quiz) with similar structure; kept
  separate to avoid touching the Question Bank delete flow.

---

## 6. Next Suggested Task

**Next task:** `o02/t04-quiz-builder-page`
**Context:** t04 replaces the `#page-quizCreate` placeholder with the real
builder. The navigation seam is ready: `navigate("quizCreate", { quizId })` is
called for New (quizId=null) and Edit (quizId set), and a `quizCreate` loader is
registered in `quiz-list.js` — t04 should move/replace that loader with the real
form module (`frontend/js/quiz-builder.js`). Use `GET /api/quizzes/<id>` (returns
`{name, questionIds, questions}`) to prefill on edit and `GET /api/questions` to
list selectable questions; save via `POST`/`PUT /api/quizzes` and surface the
`{"fields": {...}}` min-3/validation errors. The nav controller, card grid, and
delete flow from t03 stay as-is.
