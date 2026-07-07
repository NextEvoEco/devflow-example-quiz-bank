# Task: Build Question Editor And Delete Flows

**ID:** o01/t05-build-question-editor-and-delete-flows
**File:** `.devflow/tasks/o01/t05-build-question-editor-and-delete-flows.md`
**Objective Ref:** `.devflow/objective/o01-question-bank-v1.md`
**Depends On:** o01/t04-build-question-bank-list-page
**Complexity:** L
**Estimated Duration:** 90 min
**Status:** verified

---

## 1. Purpose

> What does this task accomplish within the objective?

This task completes the interactive Question Bank V1 user flows by implementing add, edit, and delete behavior through the approved modal and confirmation patterns.

---

## 2. Boundary

### In Scope

* Implement the Add Question flow.
* Implement the Edit Question flow with pre-filled data.
* Implement the Delete Question confirmation dialog and delete flow.
* Surface validation and basic error handling in the UI.
* Keep the question list in sync after create, update, and delete operations.

### Out of Scope

* Quiz Builder and Online Exam functionality.
* Advanced accessibility, multi-user, or production-hardening work beyond V1.

---

## 3. Must / Must Not

### Must

* Use the required validation rules from the confirmed interview.
* Show user-visible feedback for invalid forms or failed requests.
* Keep flows aligned with the Question Bank portion of the approved UI context.

### Must Not

* Introduce unrelated navigation or out-of-scope views.
* Bypass backend validation by relying on frontend checks alone.

---

## 4. Inputs

| Artifact | Source |
| --- | --- |
| Objective definition | `.devflow/objective/o01-question-bank-v1.md` |
| Question Bank API | `o01/t03-implement-question-bank-api` |
| Question Bank list page | `o01/t04-build-question-bank-list-page` |
| UI interaction guidance | `.devflow/context/ui-spec.md` |

---

## 5. Outputs

| Artifact | Path |
| --- | --- |
| Question editor and delete-flow frontend implementation | `frontend/` |
| Integration or UI-flow tests | `tests/` |

---

## 6. Acceptance Criteria

> These criteria must all pass before the task is marked complete.

* [x] Users can add a new question through the UI and see it appear in the list.
* [x] Users can edit an existing question and see updates reflected in the list.
* [x] Users can delete a question through a confirmation dialog and see it removed from the list.
* [x] Invalid question input is blocked and surfaced to the user with basic error feedback.

---

## 7. Test Plan

```text
1. Start the local app and open the Question Bank page.
2. Add a new valid question and verify it persists and appears in the list.
3. Edit that question and verify the updated values are shown.
4. Attempt invalid submissions and verify validation feedback appears.
5. Delete a question and verify the confirmation flow and final removal behavior.
```

---

## 8. Notes

This task should complete the primary user-visible V1 behavior.
