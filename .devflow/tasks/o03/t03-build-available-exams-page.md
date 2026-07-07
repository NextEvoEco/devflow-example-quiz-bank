# Task: Build Available Exams Page

**ID:** o03/t03-build-available-exams-page
**File:** `.devflow/tasks/o03/t03-build-available-exams-page.md`
**Objective Ref:** `.devflow/objective/o03-online-exam-v1.md`
**Depends On:** none
**Complexity:** S
**Estimated Duration:** 30 min
**Status:** verified

---

## 1. Purpose

Add the Online Exam section to the application: a sidebar navigation entry and an Available Exams page that lists all saved quizzes as exam cards. This task uses the existing `GET /api/quizzes` endpoint and produces a fully testable static page with no dependency on the new exam API.

---

## 2. Boundary

### In Scope

* Add "Online Exam" entry to the sidebar navigation.
* Implement the Available Exams page view (shown when Online Exam nav is active).
* Fetch quizzes from `GET /api/quizzes` and render each as a card: title, description, question count, Start Exam button.
* Start Exam button sets up state for the in-exam view (can navigate to exam view or set `currentView` — the exam view itself is built in t04).
* Match the approved UI mockup layout for the Available Exams page.

### Out of Scope

* In-exam question view (t04).
* Results page (t05).
* Any call to the new exam API endpoints.

---

## 3. Must / Must Not

### Must

* Reuse existing sidebar CSS and navigation switching pattern from V1/V2.
* Show an empty state message if no quizzes exist.
* Start Exam button must carry the selected `quiz_id` into the exam view state.

### Must Not

* Call `POST /api/exams/attempts` in this task (the exam API may not exist yet).
* Break existing Question Bank or Quiz Builder navigation.

---

## 4. Inputs

| Artifact                               | Source                                      |
| -------------------------------------- | ------------------------------------------- |
| Existing sidebar and nav pattern       | `frontend/index.html`, `frontend/js/app.js` |
| Existing CSS variables and card styles | `frontend/css/app.css`                      |
| UI mockup (Available Exams layout)     | `.devflow/context/ui-spec.md`               |
| Existing quiz list endpoint            | `GET /api/quizzes`                          |

---

## 5. Outputs

| Artifact                                                       | Path                                                                |
| -------------------------------------------------------------- | ------------------------------------------------------------------- |
| Updated frontend with Online Exam nav and Available Exams view | `frontend/index.html`, `frontend/js/app.js`, `frontend/css/app.css` |

---

## 6. Acceptance Criteria

* [x] "Online Exam" appears in the sidebar and activates the Available Exams view when clicked.
* [x] Available Exams view fetches quizzes from `GET /api/quizzes` and renders a card for each.
* [x] Each card shows: quiz title, description, question count, and a Start Exam button.
* [x] Start Exam button transitions the UI to the in-exam view placeholder (or stores `currentQuizId` for t04 to use).
* [x] Empty state message is shown when no quizzes exist.
* [x] Question Bank and Quiz Builder navigation remain fully functional.

---

## 7. Test Plan

```
1. Start the app.
2. Click "Online Exam" in the sidebar — Available Exams page renders.
3. Confirm quiz cards match existing quiz data.
4. Click Start Exam on one card — UI moves toward the exam view (placeholder acceptable for this task).
5. Navigate to Question Bank and Quiz Builder — confirm no regressions.
```

---

## 8. Notes

This task can be developed and verified in parallel with t01 and t02 because it only depends on the already-existing quiz API.
