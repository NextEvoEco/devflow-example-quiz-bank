# Technology Stack Context

## Purpose

Use this file to record the confirmed technology stack for the project.

## When To Fill

Fill this file once languages, frameworks, runtimes, or infrastructure choices are known.
Do not guess. Add only confirmed stack decisions.

## Confirmed Stack Decisions

### Languages

- Python for backend implementation
- TypeScript for frontend implementation (Vue single-file components)
- HTML/CSS inside Vue SFC templates and shared styles

### Frameworks And Libraries

Confirmed on this branch (`refactor/python-vue-sqlite`):

- Vue 3 (Composition API) + TypeScript for the frontend, built with Vite
- vitest for frontend unit tests

Confirmed (unchanged from the original stack):

- Flask for the Python web server and API layer
- pytest for backend automated tests
- Python standard-library `sqlite3` for database access

### Runtime And Tooling

Confirmed:

- local Python runtime
- browser-based local execution model
- SQLite local database file

Confirmed:

- Python 3.13+ local runtime
- Node.js 24+ / npm for the frontend toolchain
- `pip` with `requirements.txt` for backend dependency management
- `package.json` for frontend dependency management
- `py -m pytest` for backend tests; `npm test` (vitest) for frontend tests
- `npm run build` produces `frontend/dist/`; Flask serves the built assets

### Storage And Infrastructure

- SQLite for persisted Question Bank data
- local filesystem for project files and database file
- local web server started manually by the user

No cloud hosting, object storage, queue, cache, or external infrastructure is in scope for V1.

### Stack Constraints

- backend must be Python
- frontend is Vue 3 + TypeScript built with Vite (this branch supersedes the original
  plain HTML/CSS/JavaScript constraint — see `.devflow/intent/i04-vue-typescript-frontend.md`)
- persistence must use SQLite
- the app must remain runnable locally without external infrastructure
  (Node/npm is a build-time toolchain, not a runtime service)
- the behavior contract is preserved: same API routes and JSON shapes, same port 5000
- stack choices should preserve a clean path for later V2/V3 feature expansion
