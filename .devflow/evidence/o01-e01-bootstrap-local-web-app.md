# Evidence: Bootstrap Local Web App Foundation

**ID:** o01-e01-bootstrap-local-web-app
**Task Ref:** `.devflow/tasks/o01/t01-bootstrap-local-web-app.md`
**Executed By:** Cursor + Composer
**Execution Date:** 2026-07-12
**Execution Time:** 15:16-15:25 UTC+8, ~45 min
**Status:** completed

---

## 1. Summary

Bootstrapped the Java 21 / Spring Boot 3 Maven backend and React 18 + TypeScript (Vite) frontend.
Flyway applies `V1__baseline.sql` on startup against local PostgreSQL (`quiz_bank`). Spring Boot
listens on port 5000, serves `/api/health`, and serves the built SPA from `frontend/dist/`.
Verified with `./mvnw test`, HTTP smoke checks, and schema listing.

---

## 2. Files Changed

| File                                                           | Change Type | Description                                                          |
| -------------------------------------------------------------- | ----------- | -------------------------------------------------------------------- |
| `backend/`                                                     | created     | Spring Boot 3.5.16 Maven project with mvnw, JDBC, Flyway, PostgreSQL |
| `backend/src/main/resources/application.properties`            | created     | port 5000, datasource, Flyway, frontend dist path                    |
| `backend/src/main/resources/db/migration/V1__baseline.sql`     | created     | Flyway baseline (`schema_bootstrap`)                                 |
| `backend/src/main/java/com/quizbank/config/WebConfig.java`     | created     | static asset handler for `frontend/dist`                             |
| `backend/src/main/java/com/quizbank/web/HealthController.java` | created     | `/api/health`                                                        |
| `backend/src/main/java/com/quizbank/web/SpaController.java`    | created     | serves SPA `index.html` at `/`                                       |
| `frontend/`                                                    | created     | Vite React 18 + TypeScript app shell                                 |
| `tests/.gitkeep`                                               | created     | test directory bootstrap                                             |
| `.gitignore`                                                   | modified    | Java/Node ignore rules                                               |

---

## 3. Behavior Added

* Local app starts with `npm run build` (frontend) then `./mvnw spring-boot:run` (backend).
* Flyway migrates PostgreSQL automatically on first start.
* Minimal Quiz Bank shell page is served at `http://127.0.0.1:5000/`.
* Health endpoint confirms DB connectivity and baseline migration.

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                   | Result | Notes                                                          |
| ----------------------------------------------------------- | ------ | -------------------------------------------------------------- |
| Stable local app structure for backend, frontend, and tests | PASS   | `backend/`, `frontend/`, `tests/` present                      |
| App starts via Maven and serves a minimal page              | PASS   | `./mvnw spring-boot:run`; GET `/` → 200 HTML title "Quiz Bank" |
| Flyway migrates schema on first start without manual DDL    | PASS   | `schema_bootstrap` + `flyway_schema_history` created           |

### Test Output

```
./mvnw test → BUILD SUCCESS (contextLoads + flywayBaselineApplied)

GET http://127.0.0.1:5000/api/health
{"status":"ok","app":"quiz-bank","schemaBootstrapRows":1}

GET http://127.0.0.1:5000/ → 200, title Quiz Bank
GET http://127.0.0.1:5000/assets/*.js → 200

psql \dt → flyway_schema_history, schema_bootstrap
```

---

## 5. Known Limitations

* Domain tables (`questions`, etc.) are not created yet — deferred to o01/t02.
* Frontend is a shell only (sidebar + placeholder message).
* JDK 21 must be on PATH (`JAVA_HOME`); PostgreSQL Docker container `quiz-bank-pg` must be running.

---

## 6. Next Suggested Task

**Next task:** `o01/t02-build-question-storage-and-validation`
**Context:** Add `questions` Flyway migration, Question model, JdbcTemplate repository, validation, and repository tests. Do not wire HTTP routes yet (that is t03).
