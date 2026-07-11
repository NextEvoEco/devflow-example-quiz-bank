# Repository Structure Context

## Purpose

Use this file to explain how the repository is organized so AI can navigate it correctly.

## When To Fill

Fill this file when the repository contains meaningful code or supporting directories beyond the DevFlow starter layout.

## Current Status

The repository includes a fully runnable Quiz Bank implementation covering all three planned versions: Question Bank (V1), Quiz Builder (V2), and Online Exam (V3).

### Top-Level Directories

- `.devflow/` : DevFlow workflow state, context, templates, roles, skills, and task artifacts
- `backend/` : Python Flask server, app factory, route modules, repositories, validation, and database migrations
- `frontend/` : HTML/CSS/JavaScript client assets (`index.html`, `app.js`, `styles.css`)
- `tests/` : automated tests for the local application
- `docs/` : human-readable supporting documentation (getting-started, release/verification guides, rebuild comparison)
- `data/` : generated at runtime; stores the local SQLite database file
- `screenshots/` : browser verification captures for this rebuild (`codex_*.png`)
- root markdown files such as `README.md`, `AGENTS.md`, and `CLAUDE.md` : repository bootstrap and usage guidance

Note: `fixtures/` is git-ignored and absent on this branch. In the earlier main-line
implementation it held question-bank seed material for manual data entry and demos; this
rebuild does not carry that seed file.

### Main Application Areas

Current meaningful areas:

- `.devflow/context/` : project context documents
- `.devflow/intent/` : original request artifacts
- `.devflow/interview/` : clarification artifacts
- `.devflow/objective/` : confirmed objective artifacts
- `.devflow/tasks/` : executable task definitions
- `.devflow/evidence/` : execution and verification records
- `backend/` : Flask app factory, startup entrypoint, config, SQLite migrations, and route modules under `backend/routes/`
- `backend/exam_repository.py` : exam attempt and answer repository
- `frontend/` : Question Bank, Quiz Builder, and Online Exam views in a single `app.js` controller
- `tests/` : repository, API, page module, and release verification tests for V1–V3
- `docs/` : startup, release, and verification instructions plus the rebuild comparison

### Generated Or Derived Files

Known generated or runtime-derived items:

- `data/quiz_bank.db` : local SQLite database file created on first app start
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
