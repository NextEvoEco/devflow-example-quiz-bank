# Repository Structure Context

## Purpose

Use this file to explain how the repository is organized so AI can navigate it correctly.

## When To Fill

Fill this file when the repository contains meaningful code or supporting directories beyond the DevFlow starter layout.

## Current Status

The repository currently includes complete o01 Question Bank V1, o02 Quiz Builder V2, and o03 Online Exam V3 baselines (t01–t06 each), including release verification tests and documentation.

### Top-Level Directories

- `.devflow/` : DevFlow workflow state, context, templates, roles, skills, and task artifacts
- `backend/` : Python server, configuration, and database bootstrap
- `frontend/` : HTML/CSS/JavaScript client assets
- `tests/` : automated tests for the local application
- `docs/` : human-readable supporting documentation such as getting-started and app startup
- `data/` : generated at runtime; stores the local SQLite database file
- `screenshots/` : browser verification captures for this rebuild (`cursor_*.png`)
- root markdown files such as `README.md`, `AGENTS.md`, and `CLAUDE.md` : repository bootstrap and usage guidance

### Main Application Areas

Current meaningful areas:

- `.devflow/context/` : project context documents
- `.devflow/intent/` : original request artifacts
- `.devflow/interview/` : clarification artifacts
- `.devflow/objective/` : confirmed objective artifacts
- `.devflow/tasks/` : executable task definitions
- `.devflow/evidence/` : execution and verification records
- `backend/` : Flask app factory, startup entrypoint, config, SQLite migrations (v1 questions, v2 quizzes, v3 exams), repositories, and API routes
- `frontend/` : Question Bank, Quiz Builder, Online Exam pages, modals, and shared API helpers
- `tests/` : bootstrap, repository/validation, API, frontend page tests, and V1/V2/V3 release verification
- `docs/` : getting started, app startup, and V1/V2/V3 verification checklists

### Generated Or Derived Files

Known generated or runtime-derived items:

- `data/quiz_bank.db` : local SQLite database file
- Python cache directories such as `__pycache__/`
- `.pytest_cache/` when tests are run

### Safe Edit Areas

Typical safe edit areas:

- `.devflow/context/`
- `.devflow/intent/`
- `.devflow/interview/`
- `.devflow/objective/`
- `.devflow/tasks/`
- `.devflow/evidence/`
- `backend/`
- `frontend/`
- `tests/`
- `docs/`

### Areas Requiring Extra Caution

- `README.md`, `AGENTS.md`, and `CLAUDE.md` because they affect repository bootstrap behavior
- `.devflow/status.md` because it controls resume state
- `.devflow/memory.md` because it stores durable cross-session facts
- `.devflow/context/ui-spec.md` because it is the approved target UI context and may intentionally be ahead of the live code
- `data/quiz_bank.db` and other generated runtime files

## Interpretation Rule

When navigating this repository:

- `ui-spec.md` may describe target product scope ahead of implementation
- `backend/`, `frontend/`, and `tests/` show the current shipped code
- `status.md` tells you which slice is currently active for execution
- do not assume V2/V3 code exists until later tasks create it
