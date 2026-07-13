# Repository Structure Context

## Purpose

Use this file to explain how the repository is organized so AI can navigate it correctly.

## When To Fill

Fill this file when the repository contains meaningful code or supporting directories beyond the DevFlow starter layout.

## Current Status

**This branch (`refactor/java-react-postgre`) contains DevFlow artifacts and docs only —
no application code yet.** The layout below is the target structure the implementation
pass must produce. Do not assume `backend/` or `frontend/` exist until then.

### Top-Level Directories (target)

- `.devflow/` : DevFlow workflow state, context, templates, roles, skills, and task artifacts
- `backend/` : Java Spring Boot Maven project (`pom.xml`, `mvnw`, `src/main/java/`, `src/main/resources/db/migration/` for Flyway, `src/test/java/`)
- `frontend/` : React 18 + TypeScript application (Vite project: `src/`, `package.json`, `vite.config.ts`; `dist/` build output is git-ignored)
- `docs/` : human-readable supporting documentation (getting-started, setup prerequisites, verification guidance)
- root markdown files such as `README.md`, `AGENTS.md`, and `CLAUDE.md` : repository bootstrap and usage guidance

Note: there is no runtime `data/` directory on this branch — persisted data lives in the
local PostgreSQL service, not in a repository file.

### Main Application Areas (target)

- `.devflow/context/` : project context documents
- `.devflow/intent/` : original request artifacts
- `.devflow/interview/` : clarification artifacts
- `.devflow/objective/` : confirmed objective artifacts
- `.devflow/tasks/` : executable task definitions
- `.devflow/evidence/` : execution and verification records
- `backend/src/main/java/` : Spring Boot application, REST controllers, JdbcTemplate repositories, validation
- `backend/src/main/resources/db/migration/` : Flyway migrations (V1 questions, V2 quizzes, V3 exams)
- `backend/src/test/java/` : JUnit 5 / Spring Boot tests
- `frontend/src/` : React views/components (one view per `ui-spec.md` page id), shared state, TypeScript API client, shared styles
- `docs/` : setup (JDK, PostgreSQL), startup, and verification instructions

### Generated Or Derived Files

Known generated or runtime-derived items:

- `backend/target/` : Maven build output (git-ignored)
- `frontend/node_modules/` : npm dependencies (git-ignored)
- `frontend/dist/` : Vite build output served by Spring Boot (git-ignored)
- persisted data lives in the local PostgreSQL service (database `quiz_bank`), outside the repository

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
- generated build outputs (`backend/target/`, `frontend/dist/`) and the local PostgreSQL data

## Interpretation Rule

When navigating this repository:

- `ui-spec.md` may describe target product scope ahead of implementation
- `backend/` and `frontend/` show the current shipped code once the implementation pass
  has run — on this branch they do not exist yet
- `status.md` tells you which slice is currently active for execution
