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

- Python runtime
- SQLite database support
- browser runtime for the frontend

Currently selected in the repository:

- Flask (`flask>=3.0,<4.0`) for the local web server
- pytest (`pytest>=8.0,<9.0`) for automated tests
- Python standard-library `sqlite3` for database access

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

### Upgrade Risks

Potential future risks to track as the product grows:

- changing the Python web framework after the API shape is established
- changing the SQLite access approach after persistence tests are written
- adding a frontend framework later if the V1 code is tightly coupled to direct DOM manipulation

At the moment, these are forward-looking cautions rather than active blockers.

### Notes

- keep dependency choices lightweight for V1
- avoid unnecessary libraries before a new version milestone truly needs them
- record every chosen dependency here once it becomes part of the implementation
- when target specs expand ahead of code, do not list future dependencies here until they are actually adopted
