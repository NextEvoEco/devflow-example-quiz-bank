# Evidence: Build In-Exam Question View and Submit Flow

**ID:** o03-e04-build-exam-question-view
**Task Ref:** `.devflow/tasks/o03/t04-build-exam-question-view.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~70 min
**Status:** completed

---

## 1. Summary

Replaced the t03 `examTaking` placeholder with the real in-exam view. On Start
Exam it creates an attempt (`POST /api/exams/attempts`) and loads the quiz's
questions into frontend state, then presents one question at a time with a
progress bar, question-number jump buttons, and Previous/Next (Next becomes
Submit on the last question). Selecting an option highlights it (single-select,
checkmark) and immediately saves via `PUT .../answers/{question_id}`; previously
selected answers are restored on navigation. Submit calls `POST .../submit` and
hands the score payload to the results view (`window.examResult`), navigating to
an `examResults` placeholder (the full results UI is o03/t05). Correct answers
are never displayed during the exam. Abandoning mid-exam (navigating away) leaves
the attempt unscored with no errors. Question Bank and Quiz Builder frontends were
not touched. Verified with 129 passing tests and a full real-browser walkthrough.

---

## 2. Files Changed

| File                             | Change Type | Description                                                                                                                                                                                            |
| -------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `frontend/index.html`            | modified    | Replaced `#page-examTaking` placeholder with the real view (header, progress bar, jump numbers, question card, options, Prev/Next/Exit); added `#page-examResults` placeholder; loads `exam-taking.js` |
| `frontend/js/exam-taking.js`     | created     | Exam-taking module: create attempt, render question/options/progress/jump-numbers, immediate answer save, prev/next/jump, submit → results; registers `examTaking` + a temporary `examResults` loader  |
| `frontend/js/exam-list.js`       | modified    | Removed the temporary `examTaking` placeholder loader (ownership moved to exam-taking.js); kept Start Exam navigation                                                                                  |
| `frontend/css/style.css`         | modified    | Exam view: centered 600px column, header, progress bar, jump numbers, question card, option buttons (selected highlight + checkmark), dimmed Previous                                                  |
| `tests/test_exam_taking_page.py` | created     | 6 tests: markup, JS wiring, ownership moved, no correct-marker leak, V1/V2 untouched, full API flow                                                                                                    |
| `tests/test_v1_release.py`       | modified    | Removed the obsolete exam-view-absent guard (all exam views now exist)                                                                                                                                 |
| `tests/test_o02_release.py`      | modified    | Same removal                                                                                                                                                                                           |

---

## 3. Behavior Added

* Start Exam creates an attempt and loads the first question with four labeled options.
* Progress bar fills `(currentQuestion+1)/total`; the label reads "Question N of M".
* Question-number buttons jump to any question (satisfies free navigation); the
  current one is highlighted, answered ones are marked. Previous/Next also move
  one step; Previous is dimmed and inert on the first question.
* Selecting an option highlights it (single-select, primary label + checkmark)
  and immediately saves it via the answers API.
* Returning to a visited question restores the saved selection.
* On the last question the Next button reads "Submit"; Submit scores the attempt
  and navigates to the results view with the payload in `window.examResult`.
* Navigating away before submit abandons the attempt (stays unscored) with no error.
* The correct answer is never rendered during the exam.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                | Result | Notes                                                                          |
| ------------------------------------------------------------------------ | ------ | ------------------------------------------------------------------------------ |
| Starting an exam creates an attempt via API and loads the first question | PASS   | Browser: `POST /api/exams/attempts` → 201; Q1 with 4 options rendered          |
| Questions display with labeled options; selected option is highlighted   | PASS   | Option B highlighted with checkmark (screenshot)                               |
| Selecting an option calls the save-answer API immediately                | PASS   | `PUT .../answers/{qid}` on each click (network)                                |
| Previous/Next navigate; previously selected answers are restored         | PASS   | Jumped back to Q2 → saved "A" restored; corrected to "C"                       |
| Question progress indicator shows current position                       | PASS   | "Question N of 4" + progress bar 25%→100%                                      |
| Submit calls the submit API and passes the payload to the results view   | PASS   | Submit → `examResults`, `window.examResult` = {score:4,total:4,100%,4 answers} |
| Navigating away before submit does not error or crash                    | PASS   | Answered Q1 → went to Question Bank (4 rows) → back to exam list, no error     |

### Test Output

```
$ python -m pytest -q
129 passed in 3.69s

# Live browser walkthrough (4-question "Sample Exam", correct B/C/B/A):
- Start Exam -> attempt created; Q1 "What is 2+2?", 4 options, progress "1 of 4" 25%, Previous dimmed
- select B -> highlighted + checkmark; Q1 jump button marked answered
- Next through Q2..Q4; last question Next label = "Submit"; progress 100%
- jump back to Q2 -> saved answer restored; reselect corrects it
- Submit -> Results view; window.examResult {score:4,total:4,percentage:100}; placeholder "Score: 4 / 4 (100%)"
- abandon test: answer Q1, navigate to Question Bank (intact), back to exam list -> no crash
- console errors: none
```

Note: an earlier verification run hit repeated API `500`s ("no such table") caused
by seeding the DB from a separate process while the debug-reloader dev server held
the same SQLite file. Resolved by stopping the server, clearing the DB, restarting
fresh, and seeding through the running server's own API. Not an application bug —
all 129 tests pass against isolated per-test databases.

---

## 5. Known Limitations

* `examResults` is a minimal placeholder (score line + Back to Exams); the full
  results UI (score ring, correct/incorrect cells, Answer Review, Retry) is o03/t05.
* Exam questions are sourced from `GET /api/quizzes/<id>`, whose payload includes
  `correct` (V2, unchanged); the taking view deliberately never renders it. This
  is the documented o03/t02 limitation.

---

## 6. Next Suggested Task

**Next task:** `o03/t05-build-results-page` (final V3 build task)
**Context:** The submit payload is ready in `window.examResult` =
`{score, total, percentage, answers:[{question_id, question_text, options,
selected_option, correct_option, is_correct}]}`, and `window.examResultQuiz` =
`{id, name}`. t05 should replace the temporary `examResults` loader (registered in
`exam-taking.js`) with a real module (`frontend/js/exam-results.js`) rendering the
`ui-spec.md` results page: circular score ring (green ≥70 / amber 50–69 / red <50),
correct/incorrect count cells, per-question Answer Review (your answer, and correct
answer only when wrong), plus Back to Exams → `examList` and Retry Quiz → fresh
`examTaking` for the same quiz (`window.examResultQuiz.id`). See `.devflow/memory.md`
for the nav controller.
