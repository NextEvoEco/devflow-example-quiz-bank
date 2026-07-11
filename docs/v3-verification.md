# Quiz Bank V3 Release Verification

## Purpose

This guide describes how to verify the Online Exam V3 release baseline on top of the existing Question Bank and Quiz Builder functionality.

Use it when you want to confirm that the full Quiz Bank application is runnable, testable, and demonstrable from a fresh local checkout.

---

## 1. V3 Scope

Included in V3:

- Everything from V1 Question Bank
- Everything from V2 Quiz Builder
- Available Exams page
- Exam attempt creation and answer persistence
- In-exam question navigation with immediate answer saving
- Exam submission and score calculation
- Results page with score summary and answer review

Explicitly not included in V3:

- Historical result browsing
- Multi-user tracking or authentication
- Sharing, exporting, or printing results
- Timers or time-limited exams

---

## 2. Install And Start

Install dependencies:

```text
py -m pip install -r requirements.txt
```

Start the app:

```text
py -m backend
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 3. Run Automated Checks

```text
py -m pytest tests -v
```

This covers:

- Question Bank regression checks
- Quiz Builder schema, API, and shell checks
- Online Exam schema, API, list, taking, and results shell checks
- V1, V2, and V3 release verification tests

---

## 4. Manual Walkthrough

Use this walkthrough to validate the full V3 flow:

1. Open Question Bank and create at least 4 questions.
2. Open Quiz Builder and create a quiz containing at least 3 questions.
3. Return to Online Exam and confirm the quiz appears on the Available Exams page.
4. Click `Start Exam`.
5. Confirm the first question loads with four answer choices and a progress indicator.
6. Select an answer, move to the next question, then navigate back and confirm the previous answer is still selected.
7. Complete the remaining questions and click `Submit`.
8. Confirm the results page shows:
   - the quiz title
   - `Exam Complete!`
   - score percentage
   - correct and incorrect counts
   - per-question answer review
9. Click `Retry Quiz` and confirm a fresh exam session starts for the same quiz.
10. Click `Back to Exams` and confirm you return to the Available Exams page.
11. Navigate to Question Bank and Quiz Builder and confirm both areas still work without regression.

---

## 5. Data Reset

The local database is stored at:

```text
data/quiz_bank.db
```

To reset the demo state, stop the app and remove the database file:

```text
Remove-Item data\\quiz_bank.db
```

The next startup recreates the schema automatically.

---

## 6. Release Readiness Outcome

V3 is considered releaseable when all of the following are true:

- `py -m pytest tests -v` passes
- the local app starts with `py -m backend`
- Available Exams lists saved quizzes
- exam attempts can be started, answered, and submitted locally
- the results page shows score summary and answer review
- Question Bank and Quiz Builder behavior still work without regression
