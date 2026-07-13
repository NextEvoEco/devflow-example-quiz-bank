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

**This branch (`refactor/java-react-postgre`) contains no application code yet.**
The DevFlow artifacts have been aligned to the target stack; the implementation pass
(driven by `context/` and `tasks/`) follows. Do not assume `backend/`, `frontend/`, or
test code exist until that pass runs.

Target scope to deliver (same product as the original build, full-stack replacement):

- local web application
- Java 21 backend with Spring Boot 3
- React 18 + TypeScript frontend, built with Vite
- PostgreSQL persistence via Flyway migrations, keeping the shared logical schema
  (questions, quizzes, quiz_questions, exam_attempts, exam_answers)
- Question Bank list, search, add, edit, and delete flows
- Quiz Builder create, edit, preview, and delete flows
- Online Exam attempt, answer saving, submit, and results review flows

## Target System Overview

The target product is a small local web application with a browser-based frontend and a Java (Spring Boot) server backend.

The final UI and product behavior are described in `.devflow/context/ui-spec.md`.

The backend serves the built React frontend assets (Vite `dist/` output), exposes the API endpoints, and persists data in PostgreSQL. Later product areas may reuse the same local-app pattern as scope expands.

Each shipped version should remain independently runnable and usable on a local machine.

## Target Implementation Overview

The implementation pass on this branch must deliver all three slices: Question Bank (V1), Quiz Builder (V2), and Online Exam (V3).

When implemented:

- the frontend renders Question Bank, Quiz Builder, and Online Exam views as a React 18 + TypeScript SPA, built by Vite into `frontend/dist/` and served by Spring Boot
- the backend exposes `/api/questions`, `/api/quizzes`, and `/api/exams` route groups via Spring controllers
- persistence is handled through JdbcTemplate-based repositories (question, quiz, exam attempt) against PostgreSQL
- the schema is created and versioned by Flyway migrations under `backend/src/main/resources/db/migration/`
- the app is started locally with `npm run build` (in `frontend/`) then `./mvnw spring-boot:run` (in `backend/`), listening on port 5000

## Major Components

### Frontend

- React 18 function components written in TypeScript
- one view component per page id in `ui-spec.md` (questions, quizList, quizCreate, examList, examTaking, examResults) sharing a persistent layout shell (sidebar + top bar)
- in-page view switching per `ui-spec.md` (single `currentPage` state; no URL routing required)
- shared state for cross-view data (e.g. current exam attempt) via React context or a small store
- Vite dev server for development; `npm run build` emits `frontend/dist/` for Spring Boot to serve

Target-forward note:

- `ui-spec.md` remains the product behavior spec; it describes views and interactions, not the component framework

### Backend

- Spring Boot 3 application (Maven project under `backend/`, code in `src/main/java/`)
- HTTP layer for Question Bank (`/api/questions`), Quiz Builder (`/api/quizzes`), and Online Exam (`/api/exams`) via Spring `@RestController`s
- validation layer for question and quiz payloads
- data-access layer via JdbcTemplate repositories (question, quiz, exam attempt)
- `server.port=5000` to preserve the behavior contract

### Database

- PostgreSQL database (`quiz_bank`) as a local service (native install or Docker)
- schema managed through Flyway migrations (V1 questions, V2 quizzes, V3 exams)
- tables: `questions` (`option_a..option_d`, `correct`, `difficulty`), `quizzes`, `quiz_questions`, `exam_attempts`, `exam_answers` — same logical schema as the shared dataset

### Tests

- backend: JUnit 5 + Spring Boot Test covering repositories, APIs, and release checks
- frontend: vitest unit tests
- at least one black-box smoke check against the running app (tech-stack.md §9)

## Data Flow

Expected V1 request flow:

1. User opens the local web app in a browser
2. Frontend loads the Question Bank page
3. Frontend requests question data from the Spring Boot backend
4. Backend validates input, reads or writes data in PostgreSQL, and returns results
5. Frontend updates the visible state

Mutation flow:

1. User submits add, edit, or delete actions from the UI
2. Frontend sends the request to the backend
3. Backend validates the request
4. Backend updates PostgreSQL
5. Backend returns success or error response
6. Frontend refreshes the list or shows error feedback

## Integration Points

Currently confirmed integration points:

- browser <-> Spring Boot local web server (port 5000)
- Spring Boot application <-> local PostgreSQL service (JDBC)

No external SaaS, cloud service, authentication provider, or third-party API is in scope.
The local PostgreSQL service is the one accepted piece of local infrastructure
(see `.devflow/intent/i04-java-react-postgresql.md`).

## Execution Guidance

When using this file during implementation:

- treat `.devflow/context/ui-spec.md` as the target product specification
- treat `.devflow/status.md` as the live execution boundary
- do not assume every target view in `ui-spec.md` already exists in code
- do not let context fall behind the intended product direction

## Architectural Constraints

- each shipped version must remain lightweight and releaseable
- all three planned versions (V1 Question Bank, V2 Quiz Builder, V3 Online Exam) must be
  delivered by the implementation pass on this branch
- UI behavior follows `.devflow/context/ui-spec.md`
