# Technology Stack Context

## Purpose

Use this file to record the confirmed technology stack for the project.

## When To Fill

Fill this file once languages, frameworks, runtimes, or infrastructure choices are known.
Do not guess. Add only confirmed stack decisions.

## Confirmed Stack Decisions

### Languages

- Java 21 for backend implementation
- TypeScript for frontend implementation (React function components)
- HTML/CSS inside React components and shared styles

### Frameworks And Libraries

Confirmed on this branch (`refactor/java-react-postgre`):

- Spring Boot 3.x for the web server and API layer
- Spring JDBC (`JdbcTemplate`) repositories for database access
- Flyway for schema migrations
- React 18 + TypeScript for the frontend, built with Vite
- JUnit 5 (+ Spring Boot Test) for backend tests; vitest for frontend unit tests

### Runtime And Tooling

Confirmed:

- JDK 21+ local runtime; Maven via the `mvnw` wrapper
- Node.js 24+ / npm for the frontend toolchain
- PostgreSQL 16+ as a local database service (native install or Docker container)
- `pom.xml` for backend dependency management; `package.json` for the frontend
- `./mvnw test` for backend tests; `npm test` (vitest) for frontend tests
- `npm run build` produces `frontend/dist/`; Spring Boot serves the built assets
- `server.port=5000` so the local URL stays `http://127.0.0.1:5000`

### Storage And Infrastructure

- PostgreSQL for persisted Quiz Bank data (database `quiz_bank`); connection settings
  come from configuration (e.g. `SPRING_DATASOURCE_URL`) with a documented local default
- schema versioned by Flyway migrations in `backend/src/main/resources/db/migration/`
- local web server started manually by the user

No cloud hosting, object storage, queue, cache, or hosted services are in scope. A local
PostgreSQL service (native or Docker) is the one intentionally accepted piece of local
infrastructure — this supersedes the original "no external infrastructure" constraint
(see `.devflow/intent/i04-java-react-postgresql.md`).

### Stack Constraints

- backend must be Java 21 + Spring Boot 3 (this branch supersedes the original Python
  constraint — see `.devflow/intent/i04-java-react-postgresql.md`)
- frontend is React 18 + TypeScript built with Vite (supersedes plain HTML/CSS/JavaScript)
- persistence must use PostgreSQL with Flyway migrations (supersedes SQLite), keeping the
  shared logical schema: `questions` (`option_a..option_d`, `correct`, `difficulty`),
  `quizzes`, `quiz_questions`, `exam_attempts`, `exam_answers`
- everything must run on one local machine; no cloud dependency
- the behavior contract is preserved: same API routes and JSON shapes, same port 5000
- stack choices should preserve a clean path for later V2/V3 feature expansion
