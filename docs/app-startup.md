# Application Startup

## Prerequisites

- Python 3.13 or newer
- `pip`

## Install Dependencies

From the repository root:

```bash
pip install -r requirements.txt
```

On Windows you can also use:

```powershell
py -m pip install -r requirements.txt
```

## Start The Application

From the repository root:

```bash
py -m backend
```

The server starts at `http://127.0.0.1:5000/`.

On first start, SQLite is initialized automatically at `data/quiz_bank.db`. No manual database setup is required.

## Run Tests

Run the full test suite:

```bash
py -m pytest
```

Run only the V1 release verification checks:

```bash
py -m pytest tests/test_release_verification.py -v
```

Run only the V2 release verification checks:

```bash
py -m pytest tests/test_o02_release_verification.py -v
```

Run only the V3 release verification checks:

```bash
py -m pytest tests/test_v3_release.py -v
```

## Verify V1

For the Question Bank V1 release checklist, see [v1-verification.md](v1-verification.md).

## Verify V2

For the Quiz Builder V2 release checklist, see [v2-verification.md](v2-verification.md).

## Verify V3

For the Online Exam V3 release checklist, see [v3-verification.md](v3-verification.md).

Quick smoke check:

1. Start the server with `py -m backend`.
2. Open `http://127.0.0.1:5000/` in a browser.
3. Confirm the Question Bank page loads and CRUD still works.
4. Open `http://127.0.0.1:5000/#quizzes` and create, preview, save, edit, and delete a quiz.
5. Open `http://127.0.0.1:5000/#exams`, start an exam, answer questions, and submit to view results.
6. Confirm `data/quiz_bank.db` is created after the first start.

## Current Scope

Included:

- Question Bank list, search, add, edit, and delete
- Quiz List, Quiz Builder, and Quiz Preview
- Online Exam list, in-exam taking, and results
- SQLite persistence for questions, quizzes, and exam attempts

Excluded:

- practice mode, timed exams, and attempt history UI
- authentication and cloud deployment
