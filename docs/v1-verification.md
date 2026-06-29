# Quiz Bank V1 Verification

This guide verifies the releaseable Question Bank V1 baseline for the DevFlow example project.

## Prerequisites

- Python 3.11 or newer
- Dependencies installed from `requirements.txt`

## 1. Run Automated Checks

From the repository root:

```bash
py -m pip install -r requirements.txt
py -m pytest
```

Expected result: all tests pass.

The release suite in `tests/test_v1_release.py` covers:

- local startup and health check
- empty question bank on first run
- SQLite persistence
- list, search, create, update, and delete baseline
- validation rules and default difficulty
- exclusion of Quiz Builder and Online Exam routes

## 2. Start The Application

```bash
py -m backend
```

Open `http://127.0.0.1:5000`.

On first start, the app creates `data/quiz_bank.db` automatically. No manual database setup is required.

## 3. Manual Question Bank Checklist

Use this checklist in the browser:

1. Confirm the Question Bank page loads with search, list area, and Add Question button.
2. Confirm the empty state appears when no questions exist.
3. Add a valid question and confirm it appears in the list.
4. Search for part of the question text and confirm the list filters.
5. Edit the question and confirm the updated text and difficulty appear.
6. Submit an invalid question (for example, blank question text) and confirm error feedback appears.
7. Delete the question through the confirmation dialog and confirm it disappears from the list.
8. Confirm Quiz Builder and Online Exam navigation items remain disabled.

## 4. V1 Scope Confirmation

V1 includes:

- Question Bank list, search, add, edit, and delete
- Python backend with SQLite persistence
- plain HTML/CSS/JavaScript frontend
- basic validation and automated tests

V1 excludes:

- Quiz Builder
- Online Exam
- authentication or multi-user behavior
- cloud deployment

## 5. Release Condition

Question Bank V1 is ready to demonstrate when:

- `py -m pytest` passes
- `py -m backend` starts successfully
- the manual checklist above passes in a browser

For installation details, see [app-startup.md](app-startup.md).
