# Evidence: Build Question Bank List Page

**ID:** o01-e04-question-bank-list-page
**Task Ref:** `.devflow/tasks/o01/t04-build-question-bank-list-page.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~40 min
**Status:** completed

---

## 1. Summary

Built the visible Question Bank page: the persistent layout shell (220 px sidebar + 56 px top bar per `ui-spec.md`), a page header with title, total-count badge, and Add Question button, a left-aligned search box, an API-driven question table with colour-coded difficulty badges, and an empty state. The list is populated from `GET /api/questions` (no hardcoded data); search calls `GET /api/questions?search=` with a small debounce and updates the table in real time, swapping in a context-aware empty state when there are no matches. Add/Edit/Del controls are rendered as visible actions but wired to placeholders — the modal and delete flows are the scope of `o01/t05`. Verified with 37 passing tests plus a live browser session that rendered seeded questions, filtered on search, and showed the empty state.

---

## 2. Files Changed

| File                               | Change Type | Description                                                                                                                         |
| ---------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/index.html`              | modified    | Full Question Bank shell: sidebar nav, top bar, page header + count badge + Add button, search box, question table, empty state     |
| `frontend/css/style.css`           | modified    | Layout shell, sidebar, table, difficulty badges (Easy/Medium/Hard), buttons, search box, empty state styling                        |
| `frontend/js/app.js`               | modified    | Fetch + render questions, real-time debounced search, empty-state handling, difficulty badges; add/edit/delete placeholders for t05 |
| `backend/__main__.py`              | modified    | Honor a `PORT` env var (default 5000) so the app can bind an assigned port                                                          |
| `.claude/launch.json`              | created     | Preview launch config for `python -m backend` (autoPort)                                                                            |
| `tests/test_question_bank_page.py` | created     | Smoke checks: page shell served, static assets, API-driven list/search                                                              |

---

## 3. Behavior Added

* Opening `/` renders the Question Bank page with the sidebar/top-bar shell; Question Bank is the active nav item, Quiz Builder and Online Exam are present but inactive (their views ship in V2/V3).
* The question table renders one row per question: question text, a colour-coded difficulty badge, and Edit/Del actions.
* The total-count badge reflects the number of currently displayed questions.
* Typing in the search box filters the list in real time (case-insensitive substring via the API).
* When no questions match, an empty state replaces the table with a message specific to whether a search is active or the bank is empty.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                                 | Result | Notes                                                                                           |
| ----------------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------- |
| Users can open the local app and view the Question Bank page in the browser               | PASS   | Live preview server rendered the full page; screenshot captured                                 |
| The page renders question rows with text, difficulty, and visible actions                 | PASS   | 4 seeded questions rendered with Easy/Medium/Hard badges and Edit/Del buttons                   |
| Search updates the visible list and shows the empty state correctly when no matches exist | PASS   | "france" → 1 row; "zzznomatch" → empty state "No questions match ..."; count badge updated live |

### Test Output

```
$ python -m pytest tests/ -q
.....................................                                    [100%]
37 passed in 0.56s

# Live browser verification (preview server):
- snapshot: 4 question rows with difficulty badges + Edit/Del actions
- fill #search-input "france"     -> count 1, table shows only "What is the capital of France?"
- fill #search-input "zzznomatch" -> count 0, table hidden, empty state "No questions match \"zzznomatch\"."
- console errors: none
```

---

## 5. Known Limitations

* Add/Edit/Del buttons are visible but non-functional placeholders (log to console); the Question Editor modal and delete confirmation are `o01/t05`.
* Sidebar Quiz Builder / Online Exam items are inert placeholders (out of scope for V1).
* Frontend verification is a Python smoke check plus manual browser driving; there is no in-repo headless JS test runner (kept aligned with the project's pytest-only setup).

---

## 6. Next Suggested Task

**Next task:** `o01/t05-build-question-editor-and-delete-flows`
**Context:** `frontend/js/app.js` exposes `openAddPlaceholder`, `openEditPlaceholder(question)`, and `openDeletePlaceholder(question)` as the seams to replace with real flows. The editor should POST `/api/questions` (add) or PUT `/api/questions/<id>` (edit) and surface the API's `{"fields": {...}}` validation errors; delete should DELETE `/api/questions/<id>` behind a confirmation dialog, then call `loadQuestions()` to refresh. The Question Editor modal and Delete dialog specs are in `ui-spec.md` (fields, 540 px / 360 px widths).
