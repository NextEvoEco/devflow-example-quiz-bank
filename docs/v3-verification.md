# Online Exam V3 Verification

This guide verifies the releaseable Online Exam V3 feature for the DevFlow example project.

## Prerequisites

- Python 3.11 or newer
- Dependencies installed from `requirements.txt`
- At least one quiz with 3 or more questions (create via Quiz Builder if needed)

## 1. Run Automated Checks

From the repository root:

```bash
py -m pip install -r requirements.txt
py -m pytest tests/ -v
```

Expected result: all tests pass.

The release suite in `tests/test_v3_release.py` covers:

- full exam API lifecycle (create attempt, save answers, submit, verify score and DB state)
- abandoned attempts remaining unscored in the database
- Online Exam frontend shell and asset availability
- Question Bank regression after exam operations
- Quiz Builder regression after exam operations

Existing suites still verify:

- exam API edge cases (`tests/test_exam_api.py`)
- exam repository and schema (`tests/test_exam_repository.py`)
- exam list, taking, and results page modules
- Question Bank V1 baseline (`tests/test_v1_release.py`)
- Quiz Builder V2 baseline (`tests/test_o02_release.py`)

## 2. Start The Application

```bash
py -m backend
```

Open `http://127.0.0.1:5000`.

## 3. Manual Online Exam Checklist

Use this checklist in the browser:

1. Open **Online Exam** from the sidebar and confirm the **Available Exams** page loads.
2. Confirm each saved quiz appears as a card with title, description, question count, and **Start Exam**.
3. If no quizzes exist, confirm the empty state appears and **Go to Quiz Builder** works.
4. Click **Start Exam** on a quiz and confirm the first question loads with four option buttons.
5. Select an option and confirm it is highlighted.
6. Use **Next**, **Previous**, and the numbered jump buttons to move between questions; confirm prior selections are restored.
7. On the last question, click **Submit** and confirm the results page shows:
   - quiz title and **Exam Complete!**
   - score percentage ring and correct/incorrect counts
   - Answer Review with green correct and red incorrect rows
8. Click **Retry Quiz** and confirm a fresh exam starts on the same quiz.
9. Complete or exit the retry, then click **Back to Exams** and confirm the Available Exams listing returns.
10. Open **Exit** during an in-progress exam and confirm you return to Available Exams without errors.
11. Return to **Question Bank** and confirm list, search, add, edit, and delete still work.
12. Return to **Quiz Builder** and confirm quiz list, create, edit, preview, and delete still work.

## 4. V3 Scope Confirmation

Online Exam V3 includes:

- Available Exams listing from saved quizzes
- in-exam question view with free navigation
- immediate answer saving per question
- submit scoring with results review
- Retry Quiz and Back to Exams actions
- exam attempt persistence on submit only

Online Exam V3 excludes:

- practice mode or timed exams
- exam attempt history listing
- authentication or multi-user isolation
- changes to Question Bank or Quiz Builder behavior

## 5. Release Condition

Online Exam V3 is ready to demonstrate when:

- `py -m pytest tests/ -v` passes
- `py -m backend` starts successfully
- the manual checklist above passes in a browser
- Question Bank V1 and Quiz Builder V2 behavior remain intact

For earlier module checks, see [v1-verification.md](v1-verification.md) and [v2-verification.md](v2-verification.md).
