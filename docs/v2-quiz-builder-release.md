# Quiz Bank V2 Release Verification

## Purpose

This guide describes how to verify the Quiz Builder V2 release baseline on top of the existing Question Bank functionality.

Use it when you want to confirm that Quiz Builder is runnable, testable, and demonstrable from a fresh local checkout.

---

## 1. V2 Scope

Included in V2:

- Everything from V1 Question Bank
- Quiz list page
- Quiz create flow
- Quiz edit flow
- Quiz delete flow
- Ordered question selection and reordering
- Quiz preview from current builder state
- Quiz API and SQLite persistence

Explicitly not included in V2:

- Online Exam runtime
- browser compatibility testing beyond the development browser
- exporting, printing, or sharing quizzes

Online Exam still appears in the sidebar as the next planned product area, but it remains disabled in V2.

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
- Quiz schema and Quiz API checks
- Quiz List / Quiz Builder / Quiz Preview shell checks
- V1 and V2 release verification tests

---

## 4. Manual Walkthrough

Use this walkthrough to validate the full V2 flow:

1. Open the Question Bank and create at least 4 questions.
2. Open Quiz Builder from the sidebar.
3. Click Create Quiz.
4. Enter a quiz name.
5. Add at least 3 questions from the available list.
6. Reorder the selected questions with Up and Down.
7. Click Preview and confirm the question order, options, and correct answers match the builder state.
8. Close Preview and save the quiz.
9. Confirm the quiz appears in the Quiz List with the right question count.
10. Edit the quiz, rename it, change the selected question order, and save again.
11. Delete the quiz from the Quiz List and confirm it disappears.
12. Return to Question Bank and confirm question CRUD/search still works.

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

V2 is considered releaseable when all of the following are true:

- `py -m pytest tests -v` passes
- the local app starts with `py -m backend`
- Quiz Builder create, reorder, preview, edit, and delete flows work locally
- Question Bank behavior still works without regression
- Online Exam remains unimplemented in behavior
