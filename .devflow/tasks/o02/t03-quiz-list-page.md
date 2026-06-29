# Task: Quiz List Page

**ID:** o02/t03-quiz-list-page
**File:** `.devflow/tasks/o02/t03-quiz-list-page.md`
**Objective Ref:** `.devflow/objective/o02-quiz-builder-v1.md`
**Depends On:** o02/t02-quiz-api
**Complexity:** S
**Estimated Duration:** 45 min
**Status:** verified

---

## 1. Purpose

Add a Quiz List page to the frontend so users can browse all saved quizzes and navigate to create a new quiz or manage an existing one. After this task, quizzes are visible and accessible from the main navigation.

---

## 2. Boundary

### In Scope

- Quiz List page showing all quizzes (name, question count)
- Navigation link to the Quiz List page in the existing sidebar or nav
- "Create Quiz" button linking to the Quiz Builder page (t04)
- "Edit" button per quiz linking to the Quiz Builder in edit mode (t04)
- "Delete" button per quiz with confirmation
- Empty state when no quizzes exist

### Out of Scope

- Quiz Builder form (t04)
- Quiz Preview (t05)
- Pagination or search/filter of quizzes

---

## 3. Must / Must Not

### Must

- Follow the existing application layout and navigation structure
- Load quiz list from `GET /api/quizzes`
- Delete uses `DELETE /api/quizzes/<id>` and refreshes the list on success

### Must Not

- Modify the Question Bank page or its navigation entry
- Inline-edit quiz names from this page

---

## 4. Inputs

| Artifact        | Source           |
| --------------- | ---------------- |
| Quiz API (t02)  | o02/t02-quiz-api |
| Existing layout | `frontend/`      |

---

## 5. Outputs

| Artifact            | Path        |
| ------------------- | ----------- |
| Quiz List HTML page | `frontend/` |
| Quiz List JS module | `frontend/` |

---

## 6. Acceptance Criteria

- [x] Quiz List page loads and displays all saved quizzes
- [x] Each quiz entry shows its name and question count
- [x] "Create Quiz" button navigates to the Quiz Builder page
- [x] "Edit" button navigates to the Quiz Builder with the correct quiz loaded
- [x] "Delete" button removes the quiz after confirmation and refreshes the list
- [x] Empty state message is shown when no quizzes exist
- [x] Navigation includes a link to the Quiz List page
- [x] Question Bank page and navigation are unaffected

---

## 7. Test Plan

```
py -m backend
# open browser, navigate to Quiz List page
# verify list loads, delete works, create/edit buttons navigate correctly
```

---

## 8. Notes

Keep the page consistent with the Question Bank UI style. No new CSS framework — use the existing stylesheet.
