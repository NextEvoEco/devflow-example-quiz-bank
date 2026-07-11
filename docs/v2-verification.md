# Quiz Builder V2 Verification

This guide verifies that the Quiz Builder V2 slice is release-ready on a local machine.

V2 includes:

- Quiz List page with create, edit, and delete entry points
- Quiz Builder create/edit page with question selection and reordering
- Quiz Preview with options and correct answers shown
- Quiz API persistence with ordered question references
- Question Bank V1 behavior unchanged

V2 excludes:

- Online Exam
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

For only the O02 release verification suite:

```bash
py -m pytest tests/test_o02_release_verification.py -v
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
2. Open **Quiz Builder** (`#quizzes`) and confirm the quiz list loads.
3. Click **Create Quiz** (`#quiz-create`), enter a quiz name, and add at least 3 questions.
4. Reorder selected questions with the up/down controls.
5. Click **Preview** and confirm question order, options, and correct answers match the builder.
6. Click **Back to Builder**, then **Save Quiz** and confirm the quiz appears in the list.
7. Click **Edit** on the saved quiz, rename it, add or remove a question, save again.
8. Attempt to save with fewer than 3 questions and confirm an error message appears.
9. Delete the quiz and confirm it is removed from the list.
10. Confirm **Online Exam** navigation remains disabled.

---

## 5. Persistence Check

1. Create at least one quiz in the browser.
2. Stop the server.
3. Start the server again with `py -m backend`.
4. Confirm the quiz is still present after reload.

---

## 6. Release Result

V2 is considered verified when:

- `py -m pytest` passes
- the browser checklist above passes
- SQLite persistence survives restart
- Question Bank V1 flows remain unaffected
