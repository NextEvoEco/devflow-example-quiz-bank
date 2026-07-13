# Repository Structure Context

## Purpose

Use this file to explain how the repository is organized so AI can navigate it correctly.

## When To Fill

Fill this file when the repository contains meaningful code or supporting directories beyond the DevFlow starter layout.

## Current Status

**This branch (`refactor/python-vue-sqlite`) contains DevFlow artifacts and docs only —
no application code yet.** The layout below is the target structure the implementation
pass must produce. Do not assume `backend/`, `frontend/`, or `tests/` exist until then.

### Top-Level Directories (target)

- `.devflow/` : DevFlow workflow state, context, templates, roles, skills, and task artifacts
- `backend/` : Python server, API entrypoints, configuration, and database bootstrap
- `frontend/` : Vue 3 + TypeScript application (Vite project: `src/`, `package.json`, `vite.config.ts`; `dist/` build output is git-ignored)
- `tests/` : automated backend tests (pytest); frontend tests (vitest) live under `frontend/`
- `docs/` : human-readable supporting documentation such as getting-started and verification guidance
- `data/` : generated at runtime; stores the local SQLite database file
- root markdown files such as `README.md`, `AGENTS.md`, and `CLAUDE.md` : repository bootstrap and usage guidance

### Main Application Areas (target)

- `.devflow/context/` : project context documents
- `.devflow/intent/` : original request artifacts
- `.devflow/interview/` : clarification artifacts
- `.devflow/objective/` : confirmed objective artifacts
- `.devflow/tasks/` : executable task definitions
- `.devflow/evidence/` : execution and verification records
- `backend/` : Flask app factory, startup entrypoint, config, SQLite bootstrap, and route modules under `backend/routes/`
- `frontend/src/` : Vue views/components (one view per `ui-spec.md` page id), shared state, TypeScript API client, shared styles
- `tests/` : backend bootstrap, API, repository, and release verification tests for V1–V3
- `docs/` : startup and verification instructions for the shipped versions

### Generated Or Derived Files

Known generated or runtime-derived items:

- `data/quiz_bank.db` : local SQLite database file
- Python cache directories such as `__pycache__/`
- `.pytest_cache/` when tests are run
- `frontend/node_modules/` : npm dependencies (git-ignored)
- `frontend/dist/` : Vite build output served by Flask (git-ignored)

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
- `backend/`, `frontend/`, and `tests/` show the current shipped code once the
  implementation pass has run — on this branch they do not exist yet
- `status.md` tells you which slice is currently active for execution
