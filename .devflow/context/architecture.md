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

After o03/t06, the repository has complete Question Bank V1, Quiz Builder V2, and Online Exam V3 baselines with release verification tests and documentation.

Currently implemented:

- local web application shell started by Flask
- Python backend with Flask
- plain HTML/CSS/JavaScript frontend shell
- SQLite bootstrap with versioned migrations (`schema_migrations`, questions v1, quizzes v2, exams v3)
- `QuestionRepository` and `validate_question_payload` for CRUD/search
- `QuizRepository` and quiz validation for quiz CRUD with ordered references
- `ExamAttemptRepository` for exam attempt persistence and exam API (schema v3)
- Question Bank API blueprint under `/api/questions`
- Quiz API blueprint under `/api/quizzes`
- Exam API blueprint under `/api/exams`
- Question Bank list page with search, table rendering, and empty state
- Question Editor modal (add/edit) and Delete confirmation dialog with validation feedback
- Quiz List, Quiz Builder, and Quiz Preview frontend flows
- Online Exam list, in-exam taking, and results frontend flows
- V1, V2, and V3 release verification tests and documentation

Not yet implemented in live code:

- practice mode, timed exams, attempt history UI, authentication, and cloud deployment

## Target System Overview

The target product is a small local web application with a browser-based frontend and a Python server backend.

The final UI and product behavior are described in `.devflow/context/ui-spec.md`.

The backend serves static frontend assets, exposes Question Bank API endpoints, and persists question data in SQLite. Later product areas may reuse the same local-app pattern as scope expands.

Each shipped version should remain independently runnable and usable on a local machine.

## Current Implementation Overview

The current codebase delivers the complete o01/t01–t06 Question Bank V1, o02/t01–t06 Quiz Builder V2, and o03/t01–t06 Online Exam V3 slices.

Today:

- the frontend serves Question Bank, Quiz List, Quiz Builder, Quiz Preview, and full Online Exam flows from `frontend/` via hash routing
- the backend starts with `py -m backend` and serves static assets plus `/api/health`, `/api/questions`, `/api/quizzes`, and `/api/exams`
- SQLite is initialized at `data/quiz_bank.db` with `questions` (v1), `quizzes`/`quiz_questions` (v2), and `exam_attempts`/`exam_answers` (v3)
- question persistence and validation live in `QuestionRepository` / `validation.py`
- quiz persistence and validation live in `QuizRepository` / `quiz_validation.py`
- exam attempt persistence in `ExamAttemptRepository` / `backend/models.py`
- Question Bank API routes live in `backend/routes/questions.py`
- Quiz API routes live in `backend/routes/quizzes.py`
- Exam API routes live in `backend/routes/exams.py`
- frontend flows are wired in `frontend/js/questions.js` and `frontend/js/api.js`

## Major Components

### Frontend

- plain HTML page structure
- CSS styling for the Question Bank list page
- plain JavaScript state and event handling for list/search rendering, modal flows, and hash-based page routing
- browser-side rendering for Question Bank, Quiz List, Quiz Builder, Quiz Preview, and full Online Exam flows (list, taking, results)

Target-forward note:

- `ui-spec.md` may define additional views and interactions that are not yet present in the live code

### Backend

- Python application entrypoint for local startup (`py -m backend`)
- Flask app factory in `backend/app.py`
- static frontend asset serving
- `/api/health` endpoint
- Question Bank API routes for list/search/create/update/delete
- Quiz API routes for list/create/get/update/delete with ordered question references
- Exam API routes for attempt create, answer save, and submit with scoring
- later product extensions (practice mode, timed exams, auth) are out of current scope

### Database

- SQLite database for persisted records
- migration tracking via `schema_migrations`
- `questions` table (migration v1): question text, options A–D, correct answer, difficulty
- `quizzes` table (migration v2): quiz name and created timestamp
- `quiz_questions` join table (migration v2): ordered question references per quiz
- `exam_attempts` table (migration v3): quiz reference, score, total, timestamps
- `exam_answers` table (migration v3): per-question selected options for an attempt
- later product tables beyond exams are added by subsequent objectives

### Tests

- bootstrap automated tests for health, shell page serving, and SQLite init
- validation and repository tests for Question Bank persistence
- API integration tests for Question Bank routes
- frontend smoke tests for Question Bank page markup, search support, and question flow assets
- V1 release verification tests in `tests/test_release_verification.py`
- V2 release verification tests in `tests/test_o02_release_verification.py`
- V3 release verification tests in `tests/test_v3_release.py`
- quiz schema tests in `tests/test_quiz_schema.py`
- quiz API integration tests in `tests/test_quizzes_api.py`
- exam repository tests in `tests/test_exam_repository.py`
- exam API integration tests in `tests/test_exam_api.py`
- exam list page frontend tests in `tests/test_exam_list_page.py`
- exam taking page frontend tests in `tests/test_exam_taking_page.py`
- exam results page frontend tests in `tests/test_exam_results_page.py`
- quiz list, builder, and preview frontend tests

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
- V1 is complete: Question Bank list/search/add/edit/delete with release verification
- V2 is complete: Quiz List, Quiz Builder, Quiz Preview, quiz API, and O02 release verification
- V3 is complete: Online Exam list/taking/results, exam API, and O03 release verification
- UI behavior follows `.devflow/context/ui-spec.md`
