# Task: Quiz Preview

**ID:** o02/t05-quiz-preview
**File:** `.devflow/tasks/o02/t05-quiz-preview.md`
**Objective Ref:** `.devflow/objective/o02-quiz-builder-v1.md`
**Depends On:** o02/t04-quiz-builder-page
**Complexity:** S
**Estimated Duration:** 45 min
**Status:** complete

---

## 1. Purpose

Add a Quiz Preview view that displays the full content of a quiz — each question's text, options A–D, and correct answer — in the order defined by the user. After this task, users can review a complete quiz before or after saving.

---

## 2. Boundary

### In Scope

- Preview panel or page that shows all questions in quiz order
- Each question entry displays: question text, options A–D, correct answer indicator
- Preview is accessible from the "Preview" button in the Quiz Builder (t04)
- Preview can display an unsaved (in-memory) quiz state as well as a saved quiz

### Out of Scope

- Exam-mode execution (hiding correct answers, timer, scoring)
- Printing or exporting the quiz
- Sharing or publishing the quiz

---

## 3. Must / Must Not

### Must

- Show questions in the user-defined order (matching `position`)
- Clearly mark the correct answer for each question
- Work from the in-memory quiz state in the builder (not require a prior save)

### Must Not

- Hide the correct answer (this is a builder preview, not an exam runtime)
- Modify any API or backend code beyond what t02 already provides

---

## 4. Inputs

| Artifact                | Source                    |
| ----------------------- | ------------------------- |
| Quiz Builder page (t04) | o02/t04-quiz-builder-page |
| Quiz API GET (t02)      | o02/t02-quiz-api          |

---

## 5. Outputs

| Artifact                    | Path        |
| --------------------------- | ----------- |
| Preview panel/modal or page | `frontend/` |

---

## 6. Acceptance Criteria

- [x] Clicking "Preview" in the Quiz Builder opens the preview
- [x] All selected questions are shown in order
- [x] Each question displays text, options A–D, and the correct answer
- [x] Preview reflects the current in-builder question order (including unsaved changes)
- [x] User can close/dismiss the preview and return to the builder

---

## 7. Test Plan

```
py -m backend
# open Quiz Builder, select 3+ questions, reorder them
# click Preview: verify all questions appear in the correct order with options and correct answer shown
# change order in builder, re-open preview: verify order updated
```

---

## 8. Notes

Implementing preview as a modal overlay within the builder page is simplest for V1. A separate preview page is acceptable if it better fits the existing layout pattern.
