# Intent: Java + React + PostgreSQL Stack Refactor

**ID:** i04-java-react-postgresql
**Date:** 2026-07-12
**Status:** clarified
**Source:** user prompt

---

## 1. Original Request

> What did the user ask for?

On branch `refactor/java-react-postgre`, refactor the implementation tech stack to:

- Backend: Java 21 + Spring Boot 3.x (replaces Python + Flask)
- Frontend: React 18 + TypeScript + Vite (replaces plain HTML/CSS/JavaScript)
- Database: PostgreSQL 16+ (replaces SQLite), schema managed by Flyway migrations
- Build/test tooling: Maven (`mvnw` wrapper) + JUnit 5 for the backend;
  npm + vitest for the frontend
- Startup: `npm run build` in `frontend/`, then `./mvnw spring-boot:run` in `backend/` —
  Spring Boot serves the API and the built frontend assets on port **5000**
  (`server.port=5000`, preserving the behavior contract)

Adjust `.devflow/context/*.md` to the new stack, and align all related artifacts
(interview, objective, tasks, README, docs) following the analysis and checklist in
`docs/tech-stack.md`. Markdown alignment happens first; implementation follows in a
separate pass driven by the aligned `context/` and `tasks/`.

---

## 2. Motivation

> Why does this request matter?

This is the second branch of the tech-stack refactor experiment and the
**total-migration stress test**: unlike `refactor/python-vue-sqlite` (single layer),
this branch replaces all three layers at once — language/runtime, frontend framework,
and persistence. It tests whether the DevFlow artifacts remain a sufficient
specification when nothing of the original stack survives.

---

## 3. Known Constraints

- Product behavior and DevFlow workflow stay intact; only the tech stack changes.
- Preserve the behavior contract: same API routes and JSON shapes, same port 5000,
  same user-visible flows (Question Bank / Quiz Builder / Online Exam).
- **Persisted-schema contract** (lesson from the first refactor branch): keep the same
  logical table/column names as the shared dataset — `questions`
  (`option_a..option_d`, `correct`, `difficulty`), `quizzes`, `quiz_questions`,
  `exam_attempts`, `exam_answers` — translated to PostgreSQL types via Flyway.
- **Constraint relaxation (explicit):** the original interview confirmed
  "runnable locally without external infrastructure". PostgreSQL requires a local
  database service (native install or Docker container). This branch intentionally
  supersedes that constraint; everything must still run on one local machine with no
  cloud dependency. Connection settings come from configuration
  (e.g. `SPRING_DATASOURCE_URL`), with a documented local default.
- Prerequisites not currently present in the environment: JDK 21+, Maven (or wrapper
  bootstrap), PostgreSQL. The implementation pass must document setup steps in docs/.
- Follow `docs/tech-stack.md`: artifacts first, code second (§8); reset inherited task
  states (§3.C); completion bar is §9 including a black-box smoke check.

---

## 4. Unknowns

> What still needs clarification before objective definition?

- None blocking. Internal package structure, Flyway migration layout, and React
  component structure are decided during the implementation pass within the
  constraints above.

---

## 5. Notes

The markdown-alignment pass for this intent updates: `.devflow/interview/i01`
(backend, frontend, persistence, and delivery-model decisions are all superseded),
`.devflow/objective/o01–o03`, `.devflow/tasks/o01–o03` (statuses reset; Python/Flask/
SQLite/pytest wording replaced), `README.md`, `docs/`, and `.devflow/context/*.md`
(including a framework-agnostic note in `ui-spec.md`).
