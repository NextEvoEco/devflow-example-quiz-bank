# Task: Quiz Builder Page

**ID:** o02/t04-quiz-builder-page
**File:** `.devflow/tasks/o02/t04-quiz-builder-page.md`
**Objective Ref:** `.devflow/objective/o02-quiz-builder-v1.md`
**Depends On:** o02/t03-quiz-list-page
**Complexity:** L
**Estimated Duration:** 2 hr
**Status:** complete

---

## 1. Purpose

Implement the Quiz Builder page where users can create or edit a quiz: enter a name, browse and select questions from the Question Bank, manually reorder selected questions, and save. After this task, users can fully compose a quiz from existing questions.

---

## 2. Boundary

### In Scope

- Quiz name input field
- Question browser: display all questions from the Question Bank for selection
- Selected questions panel: shows the questions added to the quiz in order
- Manual reorder controls for selected questions (up/down buttons or drag handle)
- "Add" action to move a question from the browser into the selected panel
- "Remove" action to remove a question from the selected panel
- "Save" button: calls `POST /api/quizzes` (create) or `PUT /api/quizzes/<id>` (edit)
- Client-side validation: block save and show error if fewer than 3 questions selected
- Load existing quiz data when opened in edit mode
- "Preview" button that triggers the quiz preview (t05)

### Out of Scope

- Quiz Preview implementation (t05)
- Pagination or search within the question browser
- Inline editing of question content from this page
- Any changes to the Question Bank module

---

## 3. Must / Must Not

### Must

- Prevent duplicate question selection (a question already in the quiz cannot be added again)
- Preserve manual ordering: the order in the selected panel must match the `position` values sent to the API
- Show the question text and difficulty in the browser to help users select
- Display a clear error message when save is blocked due to fewer than 3 questions
- In edit mode, pre-populate name and question list from `GET /api/quizzes/<id>`

### Must Not

- Allow the same question to appear twice in the selected panel
- Modify any Question Bank API or data
- Auto-save; save must be triggered explicitly by the user

---

## 4. Inputs

| Artifact             | Source                 |
| -------------------- | ---------------------- |
| Quiz API (t02)       | o02/t02-quiz-api       |
| Quiz List page (t03) | o02/t03-quiz-list-page |
| Question Bank API    | `backend/`             |
| Existing layout      | `frontend/`            |

---

## 5. Outputs

| Artifact               | Path        |
| ---------------------- | ----------- |
| Quiz Builder HTML page | `frontend/` |
| Quiz Builder JS module | `frontend/` |

---

## 6. Acceptance Criteria

- [x] User can enter a quiz name
- [x] Question browser shows all questions from the Question Bank
- [x] User can add a question to the selected panel
- [x] A question already selected cannot be added again
- [x] User can remove a question from the selected panel
- [x] User can reorder selected questions using up/down controls
- [x] Saving with fewer than 3 questions is blocked with a visible error message
- [x] Saving with 3 or more questions succeeds and returns to the Quiz List
- [x] Edit mode loads the existing quiz name and question order correctly
- [x] "Preview" button is present and functional (links to t05 behavior)

---

## 7. Test Plan

```
py -m backend
# open browser, navigate to Quiz Builder
# create a quiz: enter name, add 3+ questions, reorder, save
# verify quiz appears in Quiz List
# open edit mode: verify name and order are pre-populated
# attempt save with 2 questions: verify error message appears
```

---

## 8. Notes

Reorder UX: up/down arrow buttons are sufficient for V1. Drag-and-drop is not required. Keep the selected panel clearly distinct from the question browser.
