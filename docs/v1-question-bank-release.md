# Quiz Bank V1 Release Verification

## Purpose

This guide describes how to start, test, and manually verify the V1 Question Bank release.

Use it when you want to confirm that the shipped V1 scope is runnable and demonstrable from a fresh local checkout.

---

## 1. V1 Scope

Included in V1:

- Question Bank list view
- Question search by question text
- Add Question flow
- Edit Question flow
- Delete Question flow
- SQLite persistence
- Automated backend and page-shell verification tests

Explicitly not included in V1:

- Quiz Builder workflows
- Online Exam workflows
- authentication
- cloud deployment
- CI/CD automation beyond local test commands

The sidebar still shows Quiz Builder and Online Exam labels so the target product structure remains visible, but those items stay disabled in V1.

---

## 2. Install Dependencies

```text
py -m pip install -r requirements.txt
```

---

## 3. Start The App

```text
py -m backend
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Expected startup behavior:

- the Flask server starts without crashing
- `data/quiz_bank.db` is created automatically on first run
- the Question Bank page loads in the browser

---

## 4. Run Automated Checks

```text
py -m pytest
```

The suite covers:

- bootstrap startup checks
- question validation and repository behavior
- Question Bank API success and failure paths
- Question Bank page shell checks
- V1 release verification behavior

---

## 5. Manual Verification Checklist

Run these steps in a browser after the app starts:

1. Confirm the Question Bank page loads with a search box, question table, and Add Question button.
2. If the bank is empty, confirm the empty state appears.
3. Click Add Question and create a valid question.
4. Confirm the new question appears in the list.
5. Edit that question and confirm the updated text or difficulty appears in the list.
6. Try saving an invalid question with an empty required field and confirm visible error feedback appears.
7. Delete the question through the confirmation dialog and confirm it disappears from the list.
8. Type into the search box and confirm the list updates to matching questions only.

---

## 6. Data Reset Notes

The local database lives at:

```text
data/quiz_bank.db
```

If you want a clean demo state, stop the app and delete that file before restarting:

```text
Remove-Item data\\quiz_bank.db
```

The next startup recreates the database automatically.

---

## 7. Release Readiness Outcome

V1 is considered releaseable when all of the following are true:

- `py -m pytest` passes
- the local app starts with `py -m backend`
- Question Bank list, search, add, edit, and delete flows work locally
- SQLite persistence works across restarts
- Quiz Builder and Online Exam remain unimplemented in behavior for V1
