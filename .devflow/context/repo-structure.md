# Repository Structure Context

## Purpose

Use this file to explain how the repository is organized so AI can navigate it correctly.

## When To Fill

Fill this file when the repository contains meaningful code or supporting directories beyond the DevFlow starter layout.

## Current Status

The repository now includes a runnable Question Bank V1 implementation plus DevFlow planning artifacts that may point ahead to later product scope.

### Top-Level Directories

- `.devflow/` : DevFlow workflow state, context, templates, roles, skills, and task artifacts
- `backend/` : Python server, API entrypoints, configuration, and database bootstrap
- `fixtures/` : manual demo or test content files, such as question-bank seed material prepared for human entry
- `frontend/` : HTML/CSS/JavaScript client assets
- `tests/` : automated tests for the local application
- `docs/` : human-readable supporting documentation such as getting-started, app startup, and verification guidance
- `data/` : generated at runtime; stores the local SQLite database file
- root markdown files such as `README.md`, `AGENTS.md`, and `CLAUDE.md` : repository bootstrap and usage guidance

### Main Application Areas

Current meaningful areas:

- `.devflow/context/` : project context documents
- `.devflow/intent/` : original request artifacts
- `.devflow/interview/` : clarification artifacts
- `.devflow/objective/` : confirmed objective artifacts
- `.devflow/tasks/` : executable task definitions
- `.devflow/evidence/` : execution and verification records
- `backend/` : Flask app factory, startup entrypoint, config, and SQLite bootstrap
- `fixtures/` : reusable question-bank content prepared for manual input or demos
- `frontend/` : Question Bank V1 shell page and static assets
- `tests/` : bootstrap, API, flow, and release verification tests
- `docs/` : startup and verification instructions for the shipped V1 slice

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
