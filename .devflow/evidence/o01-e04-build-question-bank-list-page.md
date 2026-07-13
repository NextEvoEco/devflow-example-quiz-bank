# Evidence: Build Question Bank List Page

**ID:** o01-e04-build-question-bank-list-page
**Task Ref:** `.devflow/tasks/o01/t04-build-question-bank-list-page.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** 15:26-15:28 UTC+8, ~20 min
**Status:** completed

---

## 1. Summary

Implemented the React Question Bank list page with layout shell, search box, difficulty
badge, empty state, and table actions. Data loads from `GET /api/questions` (with `q`
query). Verified via vitest, production build, and browser smoke against the running app.

---

## 2. Files Changed

| File                                          | Change Type | Description                    |
| --------------------------------------------- | ----------- | ------------------------------ |
| `frontend/src/App.tsx`                        | modified    | wires AppShell + QuestionsPage |
| `frontend/src/App.css`                        | modified    | Question Bank layout styles    |
| `frontend/src/types.ts`                       | created     | shared TS types                |
| `frontend/src/api/questions.ts`               | created     | API client                     |
| `frontend/src/components/AppShell.tsx`        | created     | sidebar + top bar              |
| `frontend/src/components/EmptyState.tsx`      | created     | empty state                    |
| `frontend/src/components/DifficultyBadge.tsx` | created     | difficulty pill                |
| `frontend/src/pages/QuestionsPage.tsx`        | created     | list/search page               |
| `frontend/src/questionsFilter.test.ts`        | created     | vitest filter helper           |

---

## 3. Behavior Added

* Users can open Question Bank in the browser and see question rows.
* Search filters via API; empty state shows when no matches.
* Edit/Del buttons are visible (handlers wired in t05).

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                           | Result | Notes                                            |
| ----------------------------------- | ------ | ------------------------------------------------ |
| Open app and view Question Bank     | PASS   | browser at http://127.0.0.1:5000/                |
| Rows show text, difficulty, actions | PASS   | seeded question rendered; actions present        |
| Search + empty state                | PASS   | API-backed search; empty state component present |

### Test Output

```
npm test → 2 passed
npm run build → success
Browser: title Quiz Bank, Questions count badge 1, row "Smoke continent question?"
```

---

## 5. Known Limitations

* Add/Edit/Delete modals not implemented yet (o01/t05).
* Quiz Builder / Online Exam nav items intentionally omitted for V1.

---

## 6. Next Suggested Task

**Next task:** `o01/t05-build-question-editor-and-delete-flows`
**Context:** Wire Question Editor modal and Delete confirmation to the existing list callbacks.
