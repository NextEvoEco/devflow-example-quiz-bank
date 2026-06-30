# Task: Build In-Exam Question View and Submit Flow

**ID:** o03/t04-build-exam-question-view
**File:** `.devflow/tasks/o03/t04-build-exam-question-view.md`
**Objective Ref:** `.devflow/objective/o03-online-exam-v1.md`
**Depends On:** o03/t02-implement-exam-api, o03/t03-build-available-exams-page
**Complexity:** M
**Estimated Duration:** 1 hr
**Status:** verified

---

## 1. Purpose

Implement the in-exam experience: create an attempt when the user starts an exam, display one question at a time with free navigation, save each answer immediately via API, and provide a Submit button that ends the exam and transitions to the results page.

---

## 2. Boundary

### In Scope

* On Start Exam: call `POST /api/exams/attempts` to create an attempt; store `attempt_id` in frontend state.
* Render one question at a time: question text, four labeled options (A/B/C/D) as selectable buttons.
* Show question progress indicator (e.g., "Question 3 / 10").
* Previous / Next navigation buttons for free movement between questions.
* On option select: call `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}` immediately; highlight selected option.
* Previously selected answers are restored when navigating back to a question.
* Submit button (visible throughout or on last question): call `POST /api/exams/attempts/{attempt_id}/submit` and pass the response to the results view.
* If the user navigates away from Online Exam before submitting, the in-progress attempt is abandoned (no cleanup API call needed — it stays unscored in the DB).

### Out of Scope

* Results page rendering (t05).
* Any timer or time-limit logic.
* Skipping or flagging questions.

---

## 3. Must / Must Not

### Must

* Selected option must be visually distinguished from unselected options.
* Navigation must allow jumping to any question, not only adjacent ones (e.g., question number buttons or prev/next that wrap).
* Answers already saved must be visible when returning to a previously visited question.

### Must Not

* Reveal whether an answer is correct before submission.
* Block submission if some questions are unanswered (partial submission is allowed).
* Modify Question Bank or Quiz Builder frontend code.

---

## 4. Inputs

| Artifact                                       | Source                               |
| ---------------------------------------------- | ------------------------------------ |
| Exam API (attempts, answers, submit)           | `backend/routes/exams.py` (from t02) |
| Available Exams page and `currentQuizId` state | `frontend/js/app.js` (from t03)      |
| UI mockup (in-exam layout)                     | `.devflow/context/ui-spec.md`        |

---

## 5. Outputs

| Artifact                       | Path                                                                |
| ------------------------------ | ------------------------------------------------------------------- |
| In-exam view added to frontend | `frontend/index.html`, `frontend/js/app.js`, `frontend/css/app.css` |

---

## 6. Acceptance Criteria

* [x] Starting an exam creates an attempt via API and loads the first question.
* [x] Questions display with labeled options; selected option is visually highlighted.
* [x] Selecting an option calls the save-answer API immediately.
* [x] Previous and Next buttons navigate between questions; previously selected answers are restored.
* [x] Question progress indicator shows current position (e.g., "2 / 5").
* [x] Submit button calls the submit API and passes the response payload to the results view.
* [x] Navigating away from Online Exam before submitting does not produce errors or crash the app.

---

## 7. Test Plan

```
1. Start the app and open Online Exam.
2. Click Start Exam on any quiz.
3. Verify the first question loads with four option buttons.
4. Select an option — confirm it is highlighted and the answer API is called (check network tab).
5. Click Next and Previous — confirm navigation and answer restoration.
6. Click Submit — confirm the submit API is called and the view transitions.
```

---

## 8. Notes

Store the full question list (fetched alongside quiz data) in frontend state at exam start to avoid per-question API calls during navigation. The submit response from t02 contains everything the results page needs.
