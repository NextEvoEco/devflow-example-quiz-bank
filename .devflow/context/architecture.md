# Architecture Context

## Purpose

Use this file to describe the system architecture that AI should understand before making structural changes.

## When To Fill

Fill this file when the project architecture becomes known.
If architecture is still undecided, keep the headings and leave the details blank.

## Current Status

This context may intentionally describe the target architecture ahead of the current repository implementation.

Use this file as:

- target architecture reference
- current implementation boundary guide
- execution context for structural work

### Target Architecture Status

The target product architecture is confirmed at a high level by `.devflow/context/ui-spec.md`.

### Current Implementation Status

The current repository implements V1 (Question Bank), V2 (Quiz Builder), and V3 (Online Exam).

Currently implemented:

- local web application
- Python backend with Flask
- plain HTML/CSS/JavaScript frontend
- SQLite persistence (questions, quizzes, quiz_questions, exam_attempts, exam_answers)
- Question Bank list, search, add, edit, and delete flows
- Quiz Builder create, edit, preview, and delete flows
- Online Exam attempt, answer saving, submit, and results review flows

## Target System Overview

The target product is a small local web application with a browser-based frontend and a Python server backend.

The final UI and product behavior are described in `.devflow/context/ui-spec.md`.

The backend serves static frontend assets, exposes Question Bank API endpoints, and persists question data in SQLite. Later product areas may reuse the same local-app pattern as scope expands.

Each shipped version should remain independently runnable and usable on a local machine.

## Current Implementation Overview

The current codebase delivers all three planned slices: Question Bank (V1), Quiz Builder (V2), and Online Exam (V3).

Today:

- the frontend renders Question Bank, Quiz Builder, and Online Exam pages from static assets in `frontend/`
- the backend exposes `/api/questions`, `/api/quizzes`, and `/api/exams` route groups
- question persistence is handled in SQLite through `QuestionRepository`
- quiz persistence is handled through `QuizRepository`
- exam attempt and answer persistence is handled through `ExamAttemptRepository` in `backend/exam_repository.py`
- the app is started locally with `py -m backend`

## Major Components

### Frontend

- plain HTML page structure
- CSS styling for the current Question Bank implementation
- plain JavaScript state and event handling
- browser-side rendering for implemented V1 flows

Target-forward note:

- `ui-spec.md` may define additional views and interactions that are not yet present in the live code

### Backend

- Python application entrypoint for local startup
- HTTP layer for Question Bank (`/api/questions`), Quiz Builder (`/api/quizzes`), and Online Exam (`/api/exams`) APIs
- validation layer for question and quiz payloads
- data-access layer via `QuestionRepository`, `QuizRepository`, and `ExamAttemptRepository`
- routes modularized under `backend/routes/`

### Database

- SQLite database for persisted records
- schema managed through versioned migrations (v1–v4)
- tables: `questions`, `quizzes`, `quiz_questions`, `exam_attempts`, `exam_answers`

### Tests

- basic automated backend and/or integration tests
- verification of local startup, validation, and core Question Bank behavior

## Data Flow

Expected V1 request flow:

1. User opens the local web app in a browser
2. Frontend loads the Question Bank page
3. Frontend requests question data from the Python backend
4. Backend validates input, reads or writes data in SQLite, and returns results
5. Frontend updates the visible state

Mutation flow:

1. User submits add, edit, or delete actions from the UI
2. Frontend sends the request to the backend
3. Backend validates the request
4. Backend updates SQLite
5. Backend returns success or error response
6. Frontend refreshes the list or shows error feedback

## Integration Points

Currently confirmed integration points:

- browser <-> Python local web server
- Python application <-> SQLite database file

No external SaaS, cloud service, authentication provider, or third-party API is currently in scope for the live V1 implementation.

## Execution Guidance

When using this file during implementation:

- treat `.devflow/context/ui-spec.md` as the target product specification
- treat `.devflow/status.md` as the live execution boundary
- do not assume every target view in `ui-spec.md` already exists in code
- do not let context fall behind the intended product direction

## Architectural Constraints

- each shipped version must remain lightweight and releaseable
- all three planned versions (V1 Question Bank, V2 Quiz Builder, V3 Online Exam) are now complete
- UI behavior follows `.devflow/context/ui-spec.md`
