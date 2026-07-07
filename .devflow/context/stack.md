# Technology Stack Context

## Purpose

Use this file to record the confirmed technology stack for the project.

## When To Fill

Fill this file once languages, frameworks, runtimes, or infrastructure choices are known.
Do not guess. Add only confirmed stack decisions.

## Confirmed Stack Decisions

### Languages

- Python for backend implementation
- HTML for page structure
- CSS for styling
- JavaScript for frontend interaction

### Frameworks And Libraries

Confirmed at this stage:

- no frontend framework; use plain HTML/CSS/JavaScript

Confirmed:

- Flask for the Python web server and API layer
- pytest for automated tests
- Python standard-library `sqlite3` for database access

### Runtime And Tooling

Confirmed:

- local Python runtime
- browser-based local execution model
- SQLite local database file

Confirmed:

- Python 3.13+ local runtime
- `pip` with `requirements.txt` for dependency management
- `py -m pytest` for automated tests
- Flask serves static frontend assets from `frontend/`

### Storage And Infrastructure

- SQLite for persisted Question Bank data
- local filesystem for project files and database file
- local web server started manually by the user

No cloud hosting, object storage, queue, cache, or external infrastructure is in scope for V1.

### Stack Constraints

- backend must be Python
- frontend must remain plain HTML/CSS/JavaScript for V1
- persistence must use SQLite
- V1 should be runnable locally without external infrastructure
- stack choices should preserve a clean path for later V2/V3 feature expansion
