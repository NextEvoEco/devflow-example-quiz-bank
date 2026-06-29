# Quiz Builder V1 Verification

This guide verifies the releaseable Quiz Builder V1 feature for the DevFlow example project.

## Prerequisites

- Python 3.11 or newer
- Dependencies installed from `requirements.txt`

## 1. Run Automated Checks

From the repository root:

```bash
py -m pip install -r requirements.txt
py -m pytest tests/ -v
```

Expected result: all tests pass.

The release suite in `tests/test_o02_release.py` covers:

- full quiz API lifecycle (create, list, get, reorder/update, delete)
- minimum-3-questions validation on create and update
- Question Bank CRUD and search regression after quiz operations
- Quiz Builder frontend shell and asset availability
- Online Exam remaining out of scope

Existing suites still verify:

- Question Bank V1 baseline (`tests/test_v1_release.py`)
- quiz schema, API, list page, builder page, and preview modules

## 2. Start The Application

```bash
py -m backend
```

Open `http://127.0.0.1:5000`.

## 3. Manual Quiz Builder Checklist

Use this checklist in the browser:

1. Open **Quiz Builder** from the sidebar and confirm the quiz list loads.
2. Click **Create Quiz**, enter a name, and add at least 3 questions from the browser panel.
3. Reorder selected questions with **Up** / **Down** and confirm the selected panel order changes.
4. Click **Preview** and confirm questions appear in the same order with options A–D and the correct answer highlighted.
5. Click **Save Quiz** and confirm the quiz appears on the quiz list.
6. Open **Edit** on the saved quiz, rename it, add/remove a question, save, and confirm the list updates.
7. Attempt to save with fewer than 3 questions and confirm a visible error message appears.
8. Delete the quiz and confirm it disappears from the list.
9. Return to **Question Bank** and confirm list, search, add, edit, and delete still work.

## 4. O02 Scope Confirmation

Quiz Builder V1 includes:

- quiz create, read, update, delete
- question selection by reference from the Question Bank
- manual reordering of selected questions
- minimum 3 questions validation
- full quiz preview from the builder
- quiz list and builder UI

Quiz Builder V1 excludes:

- Online Exam runtime
- quiz metadata beyond name
- shuffle/random order settings
- changes to Question Bank behavior

## 5. Release Condition

Quiz Builder V1 is ready to demonstrate when:

- `py -m pytest tests/ -v` passes
- `py -m backend` starts successfully
- the manual checklist above passes in a browser
- Question Bank V1 behavior remains intact

For Question Bank V1 checks, see [v1-verification.md](v1-verification.md).
