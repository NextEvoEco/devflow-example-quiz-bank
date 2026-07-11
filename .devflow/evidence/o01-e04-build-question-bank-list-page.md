# Evidence: Build Question Bank List Page

**ID:** o01-e04-build-question-bank-list-page
**Task Ref:** `.devflow/tasks/o01/t04-build-question-bank-list-page.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Execution Time:** 16:19-16:33 UTC+8, ~14 min
**Status:** completed

---

## 1. Summary

Replaced the bootstrap placeholder UI with a real Question Bank page shell that loads question rows from `/api/questions`, supports real-time search, shows visible edit/delete actions, and handles both empty-bank and no-match states. Added a frontend shell smoke test and verified the page behavior against a clean temporary SQLite database through the live API.

---

## 2. Files Changed

| File                               | Change Type | Description                                                                                                     |
| ---------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------- |
| `frontend/index.html`              | modified    | Replaced the placeholder startup card with the Question Bank page layout, search input, table, and empty state. |
| `frontend/styles.css`              | modified    | Added page-shell, table, badge, action, and responsive styles for the Question Bank screen.                     |
| `frontend/app.js`                  | modified    | Added live question loading, search wiring, row rendering, count updates, and empty-state handling.             |
| `tests/test_question_bank_page.py` | created     | Added a smoke test for the visible Question Bank page shell structure.                                          |
| `.devflow/status.md`               | modified    | Moved runtime state to `o01/t04`, then marked it verified and pointed to `o01/t05`.                             |

---

## 3. Behavior Added

* Users can now open the local app and see a standalone Question Bank screen instead of the bootstrap placeholder.
* The page loads question rows from the backend API and displays question text, difficulty badges, and visible Edit/Del actions.
* Search now calls the API in real time and updates the visible list plus empty state messaging.
* The page now distinguishes between an empty bank and a no-search-matches state.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                                  | Result | Notes                                                                                 |
| ------------------------------------------------------------------------------------------ | ------ | ------------------------------------------------------------------------------------- |
| Users can open the local app and view the Question Bank page in the browser.               | PASS   | Verified via page shell smoke test and live `GET /` checks.                           |
| The page renders question rows with text, difficulty, and visible actions.                 | PASS   | Implemented in `frontend/app.js` and verified against seeded API data.                |
| Search updates the visible list and shows the empty state correctly when no matches exist. | PASS   | Verified through API-backed frontend logic and a clean temporary-database smoke flow. |

### Test Output

```text
> py -m pytest
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.2, pluggy-1.6.0
collected 25 items

tests\test_bootstrap.py ...                                              [ 12%]
tests\test_question_api.py .........                                     [ 48%]
tests\test_question_bank_page.py .                                       [ 52%]
tests\test_questions.py ............                                     [100%]

============================= 25 passed in 0.25s ==============================

> live smoke with temporary database
GET /api/questions -> 200 with {"items":[]}
POST /api/questions -> 201
GET /api/questions?q=Taiwan -> 200 with seeded match
GET / -> 200 with search and table shell present
```

---

## 5. Known Limitations

* The Add Question, Edit, and Del buttons are intentionally visible but not yet interactive in this task.
* This task verifies the page shell and API-backed browsing flow; modal editor and delete confirmation belong to the next task.

---

## 6. Next Suggested Task

**Next task:** `o01/t05-build-question-editor-and-delete-flows`
**Context:** The live Question Bank page is now wired to the backend and ready for mutation flows, so the next task can focus on modal create/edit interactions and delete confirmation behavior.
