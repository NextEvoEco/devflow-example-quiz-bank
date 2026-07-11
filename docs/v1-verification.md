# Question Bank V1 Verification

This guide verifies that the Question Bank V1 slice is release-ready on a local machine.

V1 includes:

- local Python web app startup
- Question Bank list, search, add, edit, and delete
- SQLite persistence
- basic validation and error handling

V1 excludes:

- Quiz Builder
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

For only the release verification suite:

```bash
py -m pytest tests/test_release_verification.py -v
```

All tests should pass.

---

## 3. Start The Application

```bash
py -m backend
```

Open `http://127.0.0.1:5000/` in a browser.

On first run, SQLite is created automatically at `data/quiz_bank.db`.

---

## 4. Manual Browser Verification

Use this checklist in the browser:

1. Confirm the Question Bank page loads with the sidebar shell.
2. Confirm the empty state appears when no questions exist.
3. Click **Add Question** and create a valid question.
4. Confirm the new question appears in the table with difficulty badge and actions.
5. Use the search box and confirm the list filters in real time.
6. Click **Edit**, change the question, save, and confirm the update appears.
7. Submit an invalid form (for example, empty question text) and confirm validation feedback appears.
8. Click **Del**, confirm in the dialog, and verify the question is removed.
9. Confirm **Quiz Builder** and **Online Exam** sidebar items remain disabled.

---

## 5. Persistence Check

1. Create at least one question in the browser.
2. Stop the server.
3. Start the server again with `py -m backend`.
4. Confirm the question is still present after reload.

---

## 6. Out-Of-Scope Confirmation

The following should not be available in V1:

- `/api/quizzes` endpoints
- `/api/exams` endpoints
- working Quiz Builder or Online Exam navigation

Automated checks for these exclusions are in `tests/test_release_verification.py`.

---

## 7. Release Result

V1 is considered verified when:

- `py -m pytest` passes
- the browser checklist above passes
- SQLite persistence survives restart
- out-of-scope product areas remain unimplemented
