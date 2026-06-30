# Task: Build Results Page

**ID:** o03/t05-build-results-page
**File:** `.devflow/tasks/o03/t05-build-results-page.md`
**Objective Ref:** `.devflow/objective/o03-online-exam-v1.md`
**Depends On:** o03/t04-build-exam-question-view
**Complexity:** S
**Estimated Duration:** 30 min
**Status:** verified

---

## 1. Purpose

Render the exam results page using the submit response payload from t04. The page shows a score summary, correct/incorrect counts, and a per-question Answer Review with correct answers highlighted. It also provides Retry Quiz and Back to Exams actions.

---

## 2. Boundary

### In Scope

* Receive and display the submit response: `{score, total, percentage, answers[]}`.
* Score summary section: percentage dial (or progress ring), correct count badge, incorrect count badge.
* Answer Review list: one row per question with question text, user's selected option, correct option, and a correct/incorrect indicator.
* Retry Quiz button: clears attempt state and restarts the exam on the same quiz (calls t04 flow again).
* Back to Exams button: returns to the Available Exams page (t03 view).
* Match the approved UI mockup layout for the results page.

### Out of Scope

* Persisting or fetching historical results.
* Sharing or exporting results.
* Any exam attempt that was not just submitted in the current session.

---

## 3. Must / Must Not

### Must

* Show the quiz title above "Exam Complete!" heading.
* Correct answers must be clearly distinct from incorrect ones (color, icon, or label).
* Both the user's answer and the correct answer must be shown for each incorrect question.

### Must Not

* Make any additional API calls to re-fetch results (use the submit response payload already in state).
* Show results from a previous session or attempt.

---

## 4. Inputs

| Artifact                                  | Source                          |
| ----------------------------------------- | ------------------------------- |
| Submit response payload in frontend state | `frontend/js/app.js` (from t04) |
| UI mockup (results layout)                | `.devflow/context/ui-spec.md`   |
| Existing CSS variables and badge styles   | `frontend/css/app.css`          |

---

## 5. Outputs

| Artifact                       | Path                                                                |
| ------------------------------ | ------------------------------------------------------------------- |
| Results view added to frontend | `frontend/index.html`, `frontend/js/app.js`, `frontend/css/app.css` |

---

## 6. Acceptance Criteria

* [x] Results page shows quiz title, "Exam Complete!" heading, score percentage, correct count, and incorrect count.
* [x] Answer Review lists every question with: question text, user's answer, correct answer (when different), and a correct/incorrect indicator.
* [x] Correct questions show a green indicator; incorrect questions show a red indicator with the correct answer highlighted.
* [x] Retry Quiz clears the current attempt and restarts the exam on the same quiz.
* [x] Back to Exams returns to the Available Exams listing page.

---

## 7. Test Plan

```
1. Complete an exam (submit via t04 flow).
2. Verify results page renders with score, counts, and Answer Review.
3. Confirm at least one correct and one incorrect answer are styled differently.
4. Click Retry Quiz — confirm exam restarts on the same quiz.
5. Click Back to Exams — confirm return to Available Exams page.
```

---

## 8. Notes

The percentage dial can be a simple SVG circle with `stroke-dashoffset` driven by the percentage value. No external chart library needed.
