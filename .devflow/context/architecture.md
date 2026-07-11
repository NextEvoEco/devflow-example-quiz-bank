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

- the frontend renders Question Bank, Quiz Builder, and Online Exam views from static assets in `frontend/` (`index.html`, `app.js`, `styles.css`)
- the backend exposes `/api/questions`, `/api/quizzes`, and `/api/exams` route groups
- question persistence is handled through `QuestionRepository`, quizzes through `QuizRepository`, and exam attempts/answers through `ExamAttemptRepository` (`backend/exam_repository.py`)
- SQLite initialization and migrations are handled in `backend/db.py`
- the app is started locally with `py -m backend`

## Major Components

### Frontend

- plain HTML page structure (`frontend/index.html`) with one hidden `page-view` section per view
- CSS styling in `frontend/styles.css`
- a single plain-JavaScript controller (`frontend/app.js`) that caches elements, binds events, and renders every view
- browser-side rendering for Question Bank, Quiz Builder, and Online Exam flows

Note:

- the JS caches DOM nodes by id at startup and calls `addEventListener` on them in `bindEvents()`; every id referenced in `app.js` must exist in `index.html`, or `bindEvents()` throws and aborts all initialization (see `.devflow/memory.md`)

### Backend

- Python application entrypoint for local startup (`py -m backend`)
- Flask app factory (`backend/app.py`)
- HTTP layer for Question Bank (`/api/questions`), Quiz Builder (`/api/quizzes`), and Online Exam (`/api/exams`), with routes under `backend/routes/`
- validation layer for question and quiz payloads
- data-access layer via `QuestionRepository`, `QuizRepository`, and `ExamAttemptRepository`

### Database

- SQLite database for persisted records
- schema managed through versioned migrations recorded in a `schema_migrations` table (versions 1–3), applied in `backend/db.py`
- tables: `questions`, `quizzes`, `quiz_questions`, `exam_attempts`, `exam_answers`
- the `questions` table stores the answer key in a `correct_answer` column (`A`–`D`)

### Tests

- automated pytest suite covering repositories, APIs, page modules, and release checks for V1–V3
- verification of local startup, validation, CRUD, quiz building, and exam scoring

## Data Flow

Typical request flow:

1. User opens the local web app in a browser
2. `app.js` initializes, binds events, and requests data from the backend (`/api/questions`, `/api/quizzes`)
3. Backend validates input, reads or writes SQLite, and returns JSON
4. Frontend renders the active view and updates the visible state

Mutation flow (add/edit/delete question, build/save quiz, take/submit exam):

1. User submits an action from the UI
2. Frontend sends the request to the matching `/api/*` endpoint
3. Backend validates, updates SQLite, and returns success or error
4. Frontend refreshes the view or surfaces error feedback

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
