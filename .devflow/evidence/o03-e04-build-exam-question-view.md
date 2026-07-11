# Evidence: Build In-Exam Question View and Submit Flow

**ID:** o03-e04-build-exam-question-view
**Task Ref:** `.devflow/tasks/o03/t04-build-exam-question-view.md`
**Executed By:** Codex
**Execution Date:** 2026-07-08
**Status:** completed

---

## 1. Summary

Replaced the Online Exam placeholder with a working in-exam frontend flow. Starting an exam now creates an attempt through the exam API, loads the selected quiz's full question list, renders one question at a time with jump navigation, saves answers immediately on selection, and submits the attempt into an `examResults` placeholder state that is ready for the dedicated results UI in the next task.

---

## 2. Files Changed

| File                             | Change Type | Description                                                                                                                     |
| -------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/index.html`            | modified    | Replaced the simple exam placeholder with a live exam-taking layout and added an `examResults` placeholder view.                |
| `frontend/app.js`                | modified    | Added exam session state, attempt creation, answer saving, question navigation, submission handling, and exam flow reset logic. |
| `frontend/styles.css`            | modified    | Added progress bar, question card, option button, jump navigation, and exam footer styling.                                     |
| `tests/test_exam_taking_page.py` | created     | Added homepage shell coverage for exam-taking and exam-results markup.                                                          |
| `.devflow/status.md`             | modified    | Advanced runtime state to `o03/t04`, then marked it verified and pointed to `o03/t05`.                                          |

---

## 3. Behavior Added

* Clicking `Start Exam` now creates an attempt through `POST /api/exams/attempts` and loads quiz questions from `GET /api/quizzes/{id}`.
* The app now stores `attempt_id`, quiz metadata, question list, current question index, and selected answers in frontend exam state.
* The in-exam view now shows:
  * quiz label and question progress copy
  * a visual progress bar
  * question jump buttons for direct navigation
  * one question at a time
  * four selectable option buttons
  * Previous / Next / Submit navigation
* Selecting an option immediately calls the save-answer API and highlights the selected choice.
* Previously selected answers remain visible when revisiting earlier questions.
* Submitting the exam calls the submit API and stores the response in frontend state before transitioning into the `examResults` placeholder view.
* Exiting or navigating away from the exam clears frontend exam state without crashing the app.

---

## 4. Acceptance Criteria Check

| Criterion                                                                | Result | Notes                                                                                        |
| ------------------------------------------------------------------------ | ------ | -------------------------------------------------------------------------------------------- |
| Starting an exam creates an attempt via API and loads the first question | PASS   | Implemented in `startExam()` using `POST /api/exams/attempts` plus `GET /api/quizzes/{id}`.  |
| Questions display with labeled options and selected option highlighting  | PASS   | Added live exam question card rendering and selected-option styling.                         |
| Selecting an option calls the save-answer API immediately                | PASS   | Implemented in `saveExamAnswer()`.                                                           |
| Previous and Next navigation restore saved answers                       | PASS   | Implemented with `currentExamQuestionIndex` and `currentExamAnswers` keyed by `question.id`. |
| Question progress indicator shows current position                       | PASS   | Added progress copy, badge, and progress bar fill updates in `renderExamQuestionView()`.     |
| Submit calls the submit API and passes response payload to results view  | PASS   | Implemented in `submitExam()` and stored in `state.examResult`.                              |
| Navigating away before submitting does not crash the app                 | PASS   | Added exam state reset/exit handling for nav buttons and exam exit actions.                  |

---

## 5. Verification

```text
py -m pytest tests/test_exam_taking_page.py -v
1 passed in 0.13s

py -m pytest tests -v
57 passed in 1.60s

node --check frontend/app.js
pass

Flask startup smoke on http://127.0.0.1:5051/
200
```

---

## 6. Notes

* The dedicated results UI is still intentionally deferred to `o03/t05`; this task only stores submit output and transitions into an `examResults` placeholder.
* The current implementation uses question jump buttons to satisfy the "free navigation" requirement without changing the rest of the app's navigation model.

---

## 7. Next Suggested Task

**Next task:** `o03/t05-build-results-page`
