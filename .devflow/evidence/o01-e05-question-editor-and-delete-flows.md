# Evidence: Build Question Editor And Delete Flows

**ID:** o01-e05-question-editor-and-delete-flows
**Task Ref:** `.devflow/tasks/o01/t05-build-question-editor-and-delete-flows.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~50 min
**Status:** completed

---

## 1. Summary

Completed the interactive Question Bank V1 flows. Added a Question Editor modal (shared by Add and Edit) with the seven form fields from `ui-spec.md`, and a Delete confirmation dialog. The editor POSTs (`add`) or PUTs (`edit`) to the API and, on a `400`, surfaces the backend's per-field validation errors inline plus a form-level message — validation is never bypassed by frontend-only checks. Delete runs behind the confirmation dialog and issues a `DELETE`. After every create/update/delete the list is refreshed from the API so the table, count badge, and empty state stay in sync. Both overlays close on Cancel, the × button, backdrop click, and Escape. Verified with 44 passing tests plus a full real-browser session exercising add, edit, invalid-submit, and delete.

---

## 2. Files Changed

| File                           | Change Type | Description                                                                                                                                                                   |
| ------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/index.html`          | modified    | Added the Question Editor modal (7 fields + footer) and the Delete confirmation dialog overlays                                                                               |
| `frontend/css/style.css`       | modified    | Modal overlay, editor modal (540 px), dialog (360 px), form fields, field/form error styles, solid danger button                                                              |
| `frontend/js/app.js`           | modified    | Replaced t04 placeholders with real add/edit/delete flows: open/close, submit → POST/PUT, field-error surfacing, delete confirm → DELETE, list refresh, Escape/backdrop close |
| `tests/test_question_flows.py` | created     | 8 tests: editor/dialog markup present, JS wires add/edit/delete + surfaces errors, and add→edit→delete + invalid lifecycle through the API                                    |

---

## 3. Behavior Added

* **Add:** Add Question (header or empty state) opens a blank editor; saving a valid question persists it and it appears in the list.
* **Edit:** Edit on a row opens the editor pre-filled; saving updates the question and the change is reflected in the list.
* **Delete:** Del opens a confirmation dialog; confirming removes the question and refreshes the list; Cancel/backdrop/Escape dismiss without deleting.
* **Validation feedback:** Invalid submissions are blocked; the API's per-field errors are shown under each field with a form-level "Please fix the highlighted fields." message, and the modal stays open.
* **Sync:** The list, count badge, and empty state refresh from the API after every mutation.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                    | Result | Notes                                                                                                                           |
| ---------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Users can add a new question through the UI and see it appear in the list    | PASS   | Browser: added "boiling point..." → count 1→2, row rendered with Medium badge                                                   |
| Users can edit an existing question and see updates reflected in the list    | PASS   | Browser: opened pre-filled editor, changed difficulty Medium→Hard, row updated to Hard                                          |
| Users can delete a question through a confirmation dialog and see it removed | PASS   | Browser: Del → dialog → Confirm → count 2→1, row removed                                                                        |
| Invalid question input is blocked and surfaced with basic error feedback     | PASS   | Browser: empty submit → per-field errors on question/a/b/c/d + form-level message; count unchanged; backend validation enforced |

### Test Output

```
$ python -m pytest tests/ -q
............................................                             [100%]
44 passed in 0.68s

# Live browser verification (preview server):
- Add: fill 7 fields, submit -> POST /api/questions 201, list refresh shows new row (count 2)
- Invalid: empty submit -> 400; field-errors shown for question,a,b,c,d; form-error visible; modal stays open
- Edit: openEdit pre-fills correctly; change difficulty -> PUT -> row shows Hard
- Delete: openDelete shows dialog "Delete Question"; confirm -> DELETE 204 -> row removed (count 1)
- console errors: none
```

Note: during verification, one interaction sequence hit a preview-reload race (a native form submit fired before the reloaded JS bound its handlers). Re-running the same flow on the settled page worked correctly and the event listeners were confirmed attached; this was a test-harness timing artifact, not an application bug.

---

## 5. Known Limitations

* The delete dialog copy states permanent removal from the bank; the `ui-spec.md` "cascade deletion from quizzes" wording is intentionally omitted because V1 has no quizzes table — that concern belongs to V2.
* No optimistic UI; the list re-fetches after each mutation (simple and correct for a local app).
* Accessibility is basic (roles/aria-modal, Escape/backdrop close) but not a full focus-trap — out of scope for V1 per the task.

---

## 6. Next Suggested Task

**Next task:** `o01/t06-add-release-checks-and-verification`
**Context:** All primary user-visible V1 Question Bank behavior is complete (list, search, add, edit, delete with validation) and covered by 44 tests across bootstrap, repository, API, page, and flow suites. t06 should add release-level checks/verification and any docs needed to declare V1 releaseable. The app runs via `py -m backend` (honors `PORT`); tests run via `py -m pytest`. A preview launch config exists at `.claude/launch.json`.
