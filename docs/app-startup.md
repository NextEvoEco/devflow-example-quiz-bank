# Application Startup

This guide covers running and verifying the Quiz Bank Question Bank V1 application.

## Prerequisites

- Python 3.11 or newer
- A local terminal

## Install Dependencies

From the repository root:

```bash
py -m pip install -r requirements.txt
```

## Start The Application

From the repository root:

```bash
py -m backend
```

The server starts at `http://127.0.0.1:5000`.

On first start, the application automatically creates:

- `data/` directory
- `data/quiz_bank.db` SQLite database
- schema migrations and the `questions` table

No manual database setup is required. The question bank starts empty.

## Run Tests

```bash
py -m pytest
```

All tests should pass before demonstrating or releasing V1.

## Verify In The Browser

1. Open `http://127.0.0.1:5000`.
2. Confirm the Question Bank page loads.
3. Add, search, edit, and delete a question to confirm the V1 flows work.
4. Confirm Quiz Builder and Online Exam remain disabled in the sidebar.

For the full release checklist, see [v1-verification.md](v1-verification.md).
