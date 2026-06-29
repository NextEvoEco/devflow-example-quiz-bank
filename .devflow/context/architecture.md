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

The current repository implements the V1 Question Bank subset only.

Currently implemented:

- local web application
- Python backend with Flask
- plain HTML/CSS/JavaScript frontend
- SQLite persistence
- Question Bank list, search, add, edit, and delete flows

Not yet implemented in the live repository:

- Quiz Builder runtime flows
- Online Exam runtime flows

Still intentionally flexible:

- exact backend package layout beyond the current bootstrap modules
- exact frontend file split beyond the current shell structure

## Target System Overview

The target product is a small local web application with a browser-based frontend and a Python server backend.

The final UI and product behavior are described in `.devflow/context/ui-spec.md`.

The backend serves static frontend assets, exposes Question Bank API endpoints, and persists question data in SQLite. Later product areas may reuse the same local-app pattern as scope expands.

Each shipped version should remain independently runnable and usable on a local machine.

## Current Implementation Overview

The current codebase delivers the Question Bank V1 slice of the target architecture.

Today:

- the frontend renders the Question Bank page from static assets in `frontend/`
- the backend exposes `/api/questions` routes
- question persistence is handled in SQLite through `QuestionRepository`
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
- HTTP layer for Question Bank APIs via `/api/questions`
- validation layer for question payloads
- data-access layer for SQLite operations via `QuestionRepository`
- `questions` SQLite table with migration v2 schema

### Database

- SQLite database for persisted question records
- schema limited to V1 Question Bank needs

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
- the current shipped version is limited to Question Bank only
- Quiz Builder and Online Exam remain target architecture areas, not current implementation scope
- the codebase should leave room for V2 and V3 expansion without forcing a rewrite
- UI behavior should follow `.devflow/context/ui-spec.md`
