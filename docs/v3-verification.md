# Online Exam V3 Verification

This guide verifies that the Online Exam V3 slice is release-ready on a local machine.

V3 includes:

- Online Exam navigation and Available Exams listing
- In-exam question view with answer selection and navigation
- Exam submit flow with scoring and results page
- Exam attempt persistence (`exam_attempts`, `exam_answers`)
- Question Bank V1 and Quiz Builder V2 behavior unchanged

V3 excludes:

- practice mode or timed exams
- exam attempt history listing
- authentication and cloud deployment

---

## 1. Install Dependencies

From the repository root:

```bash
pip install -r requirements.txt
```

On Windows:

```powershell
py -m pip install -r requirements.txt
```

---

## 2. Run Automated Release Checks

```bash
py -m pytest
```

For only the O03 release verification suite:

```bash
py -m pytest tests/test_v3_release.py -v
```

All tests should pass.

---

## 3. Start The Application

```bash
py -m backend
```

Open `http://127.0.0.1:5000/` in a browser.

---

## 4. Manual Browser Walkthrough

Use this checklist in the browser:

1. Open **Question Bank** and confirm list, search, add, edit, and delete still work.
2. Open **Quiz Builder** (`#quizzes`) and confirm quiz list, create, preview, edit, and delete still work.
3. Open **Online Exam** (`#exams`) and confirm saved quizzes appear as exam cards.
4. Click **Start Exam** on a quiz with at least 3 questions.
5. Answer questions using the option buttons; use **Previous**, **Next**, and the numbered jump buttons.
6. Confirm selected answers stay highlighted when navigating back.
7. Click **Exit** on a fresh attempt and confirm you return to Available Exams without a results page.
8. Start the exam again, answer some questions, and click **Submit** on the last question.
9. Confirm the results page shows score percentage, correct/incorrect counts, and Answer Review.
10. Click **Retry Quiz** and confirm a new exam session starts for the same quiz.
11. Complete or exit, then click **Back to Exams** and confirm the listing page loads.

---

## 5. Persistence Check

1. Complete an exam and submit it in the browser.
2. Stop the server.
3. Start the server again with `py -m backend`.
4. Confirm questions, quizzes, and submitted attempt records still exist in the local database.
5. Note: the results page only shows the latest submit payload for the current browser session.

---

## 6. Release Result

V3 is considered verified when:

- `py -m pytest` passes
- the browser checklist above passes
- SQLite persistence survives restart
- Question Bank V1 and Quiz Builder V2 flows remain unaffected
