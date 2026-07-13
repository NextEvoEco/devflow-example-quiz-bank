# Task: Bootstrap Local Web App Foundation

**ID:** o01/t01-bootstrap-local-web-app
**File:** `.devflow/tasks/o01/t01-bootstrap-local-web-app.md`
**Objective Ref:** `.devflow/objective/o01-question-bank-v1.md`
**Depends On:** none
**Complexity:** M
**Estimated Duration:** 1 hr
**Status:** completed

---

## 1. Purpose

> What does this task accomplish within the objective?

This task establishes the runnable project foundation for Quiz Bank V1 so later tasks can implement persistence, APIs, and UI on a stable local application structure.

---

## 2. Boundary

### In Scope

* Create the initial Java application structure (Spring Boot 3, Maven project) for a local web app.
* Wire a lightweight Spring Boot server setup suitable for serving API endpoints and the built React frontend assets (Vite `dist/` output) on port 5000.
* Create the base repository code layout for backend, frontend, and tests.
* Initialize the PostgreSQL schema via Flyway migrations on first start.
* Provide a minimal runnable app shell so the application can start locally.

### Out of Scope

* Full question CRUD behavior.
* Final Question Bank UI implementation.
* Quiz Builder or Online Exam features.

---

## 3. Must / Must Not

### Must

* Keep the implementation intentionally lightweight.
* Use Java 21 + Spring Boot 3 and PostgreSQL (Flyway migrations).
* Produce a startup flow that a later task can extend without restructuring the repository again.

### Must Not

* Implement Question Bank business behavior prematurely.
* Introduce out-of-scope product features or production-only infrastructure.

---

## 4. Inputs

| Artifact                      | Source                                       |
| ----------------------------- | -------------------------------------------- |
| Objective definition          | `.devflow/objective/o01-question-bank-v1.md` |
| UI context                    | `.devflow/context/ui-spec.md`                |
| Repository structure guidance | `.devflow/context/repo-structure.md`         |

---

## 5. Outputs

| Artifact                                        | Path                                         |
| ----------------------------------------------- | -------------------------------------------- |
| Spring Boot app bootstrap and server entrypoint | `backend/` (Maven project, `src/main/java/`) |
| Frontend static shell files                     | `frontend/`                                  |
| Flyway migration baseline                       | `backend/src/main/resources/db/migration/`   |
| Basic startup instructions update               | `README.md` or `docs/` as needed             |
| Test directory bootstrap                        | `tests/`                                     |

---

## 6. Acceptance Criteria

> These criteria must all pass before the task is marked complete.

* [x] The repository has a stable local app structure for backend, frontend, and tests.
* [x] The application can be started by the documented Maven command (`./mvnw spring-boot:run`) and serve at least a minimal page successfully.
* [x] Flyway migrates the PostgreSQL schema on first start without manual schema setup (a reachable local PostgreSQL service is a documented prerequisite).

---

## 7. Test Plan

```text
1. Start the local application with the documented Maven command.
2. Verify the server starts without crashing.
3. Open the app in a browser and confirm a minimal shell page is served.
4. Verify the PostgreSQL schema is migrated automatically by Flyway.
```

---

## 8. Notes

Use this task to lock the project structure so later tasks can target concrete paths without renegotiating layout decisions.
