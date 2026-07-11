# Evidence: Quiz Builder Page

**ID:** o02-e04-quiz-builder-page
**Task Ref:** `.devflow/tasks/o02/t04-quiz-builder-page.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Execution Time:** 17:32-17:45 UTC+8, ~13 min
**Status:** completed

---

## 1. Summary

Replaced the Quiz Builder placeholder with a working create/edit page that lets users name a quiz, browse available questions from the Question Bank, add and remove questions, reorder selected questions with up/down controls, and save through the live quiz API. Edit mode now loads existing quiz data, and a Preview button is present as the next-task entry point without implementing the full preview yet.

---

## 2. Files Changed

| File                              | Change Type | Description                                                                                                                                    |
| --------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/index.html`             | modified    | Replaced the Quiz Builder placeholder with the full builder form, selected/available question panels, and preview button shell.                |
| `frontend/app.js`                 | modified    | Added quiz builder state, add/remove/reorder logic, create/edit loading, save handling, validation feedback, and preview placeholder behavior. |
| `frontend/styles.css`             | modified    | Added builder layout, builder card, builder item, and dual-panel styling.                                                                      |
| `tests/test_quiz_builder_page.py` | created     | Added a page-shell smoke test for the Quiz Builder form and key controls.                                                                      |
| `.devflow/status.md`              | modified    | Moved runtime state to `o02/t04`, then marked it verified and pointed to `o02/t05`.                                                            |

---

## 3. Behavior Added

* Users can now enter a quiz name in the Quiz Builder page.
* The builder shows all available Question Bank questions and prevents adding the same question twice.
* Selected questions can now be removed or reordered with up/down controls.
* Saving is blocked with visible feedback when fewer than 3 questions are selected.
* Edit mode now loads an existing quiz name and ordered question list from `GET /api/quizzes/<id>`.
* Save now creates or updates quizzes through the live API and returns to the Quiz List page on success.
* A Preview button is now present and opens a placeholder surface for the next task.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                  | Result | Notes                                                                                                      |
| -------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------- |
| User can enter a quiz name                                                 | PASS   | Implemented in the builder form.                                                                           |
| Question browser shows all questions from the Question Bank                | PASS   | Builder uses the live Question Bank dataset already loaded from `/api/questions`.                          |
| User can add a question to the selected panel                              | PASS   | Implemented in the available-questions panel action.                                                       |
| A question already selected cannot be added again                          | PASS   | Selected questions are filtered out of the available list.                                                 |
| User can remove a question from the selected panel                         | PASS   | Implemented with Remove buttons in the selected panel.                                                     |
| User can reorder selected questions using up/down controls                 | PASS   | Implemented with Up/Down controls and preserved order state.                                               |
| Saving with fewer than 3 questions is blocked with a visible error message | PASS   | Client-side validation added and confirmed against live API expectations.                                  |
| Saving with 3 or more questions succeeds and returns to the Quiz List      | PASS   | Builder now posts to `/api/quizzes` or updates via `/api/quizzes/<id>` and returns to the list on success. |
| Edit mode loads the existing quiz name and question order correctly        | PASS   | Builder fetches quiz details and pre-populates name and ordered selection state.                           |
| "Preview" button is present and functional (links to t05 behavior)         | PASS   | Button is present and opens a clear preview placeholder for the next task.                                 |

### Test Output

```text
> py -m pytest tests -v
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 40 items
...
tests/test_quiz_builder_page.py::test_quiz_builder_page_shell_is_present PASSED
...
============================= 40 passed in 0.77s ==============================

> live builder smoke
HTML shell contains quiz-builder-form and preview button
POST invalid /api/quizzes -> 400 with minimum-question error
POST /api/quizzes -> 201
GET /api/quizzes/<id> -> existing quiz data returned for edit mode
PUT /api/quizzes/<id> -> reordered questionIds returned
```

---

## 5. Known Limitations

* I verified builder readiness through regression tests plus live HTTP/data smoke checks, but not through full browser click automation.
* The Preview button currently opens a placeholder surface; the actual quiz preview behavior belongs to `o02/t05`.

---

## 6. Next Suggested Task

**Next task:** `o02/t05-quiz-preview`
**Context:** The builder now produces ordered quiz data and edit-mode state, so the next task can focus on rendering a full preview from that live quiz context.
