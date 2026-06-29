# Coding Conventions Context

## Purpose

Use this file to record project-specific conventions that should guide implementation and review.

## When To Fill

Fill this file when style, architecture, testing, or repository conventions are known.

## Current Conventions

These conventions are confirmed from the DevFlow workflow, interview, objective, and starter repository structure.

### Code Style

- keep implementation explicit and lightweight
- prefer straightforward structure over heavy abstraction
- keep V1 code easy for a fresh AI session to understand
- use stable, readable filenames and identifiers
- keep Question Bank logic isolated from future Quiz Builder and Online Exam logic

### Testing Expectations

- V1 must include basic automated tests
- tests should cover the V1 baseline: startup, validation, persistence, and/or integration behavior
- tests should stay aligned with task acceptance criteria
- do not skip verification just because the app works manually

### Documentation Expectations

- update DevFlow artifacts when project state changes
- keep `status.md` current
- record durable, non-obvious facts in `memory.md`
- write evidence after implementation or verification work
- keep context files aligned with confirmed project decisions

### Review Expectations

- stay within the active task boundary
- do not introduce Quiz Builder or Online Exam functionality during V1 Question Bank tasks
- preserve releaseable behavior at each planned version milestone
- prefer simple local-app solutions over production-scale infrastructure
- avoid undocumented assumptions about stack or architecture

### Conventions That Must Not Be Broken

- backend must be Python
- frontend must be plain HTML/CSS/JavaScript for V1
- persistence must use SQLite
- V1 scope must remain limited to Question Bank CRUD and search
- question text, options A-D, and correct answer must be validated
- difficulty must have a default value
- every significant workflow step should be reflected in DevFlow artifacts
