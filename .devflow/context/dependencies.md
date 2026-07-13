# Dependencies Context

## Purpose

Use this file to record important project dependencies that AI should be aware of.

## When To Fill

Fill this file when dependency choices, critical integrations, or version constraints are confirmed.

## Current Status

The V1 implementation is already running with a small confirmed dependency set.

This file should reflect the live codebase first, while still noting where later expansion may add dependencies.

### Core Dependencies

Confirmed dependency categories:

- Python runtime (backend)
- Node.js runtime (frontend build toolchain only)
- SQLite database support
- browser runtime for the frontend

Currently selected on this branch:

- Flask (`flask>=3.0,<4.0`) for the local web server
- pytest (`pytest>=8.0,<9.0`) for backend automated tests
- Python standard-library `sqlite3` for database access
- Vue 3 + TypeScript for the frontend
- Vite for the frontend build/dev server
- vitest for frontend unit tests

### External Services

None are currently in scope for V1.

There is no confirmed dependency on:

- cloud APIs
- authentication providers
- hosted databases
- payment services
- messaging platforms

### Version Constraints

Confirmed versions:

- Python 3.13+
- Flask 3.x
- pytest 8.x
- SQLite via Python standard library
- Node.js 24+ / npm 11+
- Vue 3.x, Vite 5+/6+, vitest (versions pinned in `package.json` when implemented)

### Upgrade Risks

Potential future risks to track as the product grows:

- changing the Python web framework after the API shape is established
- changing the SQLite access approach after persistence tests are written
- Vue/Vite major-version upgrades once components and build config are established

At the moment, these are forward-looking cautions rather than active blockers.

### Notes

- keep dependency choices lightweight for V1
- avoid unnecessary libraries before a new version milestone truly needs them
- record every chosen dependency here once it becomes part of the implementation
- when target specs expand ahead of code, do not list future dependencies here until they are actually adopted
