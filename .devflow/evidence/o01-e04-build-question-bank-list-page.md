# Evidence: Build Question Bank List Page

**ID:** o01-e04-build-question-bank-list-page
**Task Ref:** `.devflow/tasks/o01/t04-build-question-bank-list-page.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-11
**Execution Time:** ~18:10-18:35 UTC+8, ~25 min
**Status:** completed

---

## 1. Summary

Implemented the Vue Question Bank list page (shell, table, difficulty badges, search, empty state) consuming `GET /api/questions`. Fixed Flask static routing so `static_url_path=""` no longer shadowed API routes. Verified in browser against the running app.

---

## 2. Files Changed

| File                                      | Change Type | Description                          |
| ----------------------------------------- | ----------- | ------------------------------------ |
| `frontend/src/App.vue`                    | modified    | Layout + Questions view              |
| `frontend/src/api.ts`                     | created     | Typed API client                     |
| `frontend/src/types.ts`                   | created     | Shared TS types                      |
| `frontend/src/composables/useAppState.ts` | created     | currentPage state                    |
| `frontend/src/components/*`               | created     | Sidebar, TopBar, Badge, Empty        |
| `frontend/src/views/QuestionsView.vue`    | created     | List + search                        |
| `frontend/src/styles/app.css`             | modified    | ui-spec styles                       |
| `backend/app.py`                          | modified    | Serve `/assets` without API conflict |

---

## 3. Behavior Added

* Question Bank page with list, count, search, empty state
* Edit/Del action buttons visible (mutation flows in t05)

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                           | Result | Notes                    |
| ----------------------------------- | ------ | ------------------------ |
| Open app and view Question Bank     | PASS   | Browser snapshot         |
| Rows show text, difficulty, actions | PASS   |                          |
| Search + empty state                | PASS   | Typed "france"; filtered |

### Test Output

```
npm run build — success
npm test — 1 passed
Browser: Questions table renders; search "france" shows Capital of France?
```

---

## 5. Known Limitations

* Add/Edit/Delete modals not wired yet (t05)
* Favicon 404 (harmless)

---

## 6. Next Suggested Task

**Next task:** `o01/t05-build-question-editor-and-delete-flows`
**Context:** Wire Question Editor modal and Delete confirmation to API mutations.
