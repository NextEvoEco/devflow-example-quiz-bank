# Refactor Stack Comparison

> Cross-stack analysis of the Quiz Bank refactor experiment.
>
> This document is **stack-neutral**: it compares the implementation results of
> every `refactor/*` tech-stack branch. It is intended to live on a dedicated
> comparison branch (e.g. `refactor/compare`) or on `main`, **not** inside any
> single stack branch — the comparison must not favor or be authored from one
> stack's perspective.
>
> **Placement:** this is the canonical copy on `refactor/java-react-postgre` (can
> be mirrored to `main` or a `refactor/compare` branch when ready).
>
> **Coverage note:** in the current pass, both `refactor/python-vue-sqlite` and
> `refactor/java-react-postgre` were built, verified, and compared in depth.
> Findings span both branches equally.

---

## 1. Purpose

The experiment answers a key question:

> **Given the same DevFlow specification, how differently do different technology
> stacks rebuild the same application?**

Every stack receives the identical, code-free DevFlow artifacts (intent, interview,
objective, tasks) and must reconstruct the Quiz Bank application from them alone.
Differences between the branches are therefore attributable to the stack choice
(language, frameworks, database) and the tools' interpretation, not to differing
requirements.

---

## 2. Shared Baseline

| Item                 | Value                                                                               |
| -------------------- | ----------------------------------------------------------------------------------- |
| Baseline branch      | `refactor/base`                                                                     |
| Baseline commit      | `43b8f8d`                                                                           |
| Baseline contents    | DevFlow artifacts only — **no application code**                                    |
| Frozen specification | `.devflow/intent/`, `.devflow/interview/`, `.devflow/objective/`, `.devflow/tasks/` |

Each stack branch is a single implementation commit on top of this baseline.

---

## 3. Branch ↔ Stack Map

| Branch                        | Backend               | Frontend              | Persistence       | Impl commit (current tip) |
| ----------------------------- | --------------------- | --------------------- | ----------------- | ------------------------- |
| `refactor/base`               | —                     | —                     | —                 | `43b8f8d`                 |
| `refactor/python-vue-sqlite`  | Python + Flask        | Vue 3 + TypeScript    | SQLite            | `dba729a`                 |
| `refactor/java-react-postgre` | Java 21 + Spring Boot | React 18 + TypeScript | PostgreSQL+Flyway | `5a54cd3`                 |

Notes:

- Each implementation commit was verified in this session — both apps were built,
  started, and tested in-browser. All 18 task acceptance criteria were verified per
  the task definitions.
- Metrics in §6 are from the clean implementation (code areas only: `backend/`,
  `frontend/`, `tests/`).

---

## 4. Naming Convention

Stack-specific outputs are prefixed with the stack's short identifier so results
from different branches never collide when gathered together:

| Prefix    | Branch                        | Examples                                    |
| --------- | ----------------------------- | ------------------------------------------- |
| `python_` | `refactor/python-vue-sqlite`  | `screenshots/python_question_bank_list.png` |
| `java_`   | `refactor/java-react-postgre` | `screenshots/java_question_bank_list.png`   |

Per-stack artifacts (`screenshots/*_*.png`, evidence files) **stay on their own
stack branch**. This comparison branch (or a dedicated `refactor/compare`) only
*aggregates or references* them.

---

## 5. Comparison Methodology

How to reproduce each measurement:

```bash
# Files a stack added on top of the shared baseline (excluding DevFlow artifacts)
git diff --name-only refactor/base refactor/python-vue-sqlite | grep -v '^.devflow/'
git diff --name-only refactor/base refactor/java-react-postgre | grep -v '^.devflow/'

# Code volume (application areas only)
git diff --shortstat refactor/base refactor/python-vue-sqlite -- backend frontend tests
git diff --shortstat refactor/base refactor/java-react-postgre -- backend frontend tests

# Language file counts
git ls-tree -r --name-only refactor/python-vue-sqlite -- backend/ | grep '\.py$' | wc -l
git ls-tree -r --name-only refactor/java-react-postgre -- backend/ | grep '\.java$' | wc -l

# Full side-by-side of two stacks
git diff refactor/python-vue-sqlite refactor/java-react-postgre -- backend frontend tests
```

Dimensions worth comparing:

- **Architecture** — module granularity, file layout, separation of concerns, persistence layer
- **Volume** — lines of code, file count (proxy, not a quality score)
- **Database choice** — schema design, migration strategy, query patterns
- **Frontend structure** — component organization, state management, styling approach
- **Test coverage** — number and shape of tests, what they exercise
- **Spec adherence** — did each task boundary get honored; any scope drift
- **Correctness** — do all suites pass; behavior parity in the browser
- **Infrastructure** — setup complexity, runtime dependencies, local-dev ergonomics

---

## 6. Quantitative Results

Measured against `refactor/base` (baseline has no code), covering code areas
(`backend/`, `frontend/`, `tests/`).

| Metric                                            | Python + Vue + SQLite            | Java + Spring Boot + PostgreSQL  |
| ------------------------------------------------- | -------------------------------- | -------------------------------- |
| Backend files added                               | 13 `.py` files                   | 26 `.java` files                 |
| Frontend files added                              | 27 files (`*.js`,`*.vue`,`*.ts`) | 32 files (`.tsx`, `.ts`)         |
| Test files added                                  | 8 `test_*.py` files              | 19 `*Test.java` files            |
| Insertions in code areas                          | 8,135                            | 6,481                            |
| Configuration files (pom.xml, package.json, etc.) | 4                                | 6 (Maven wrapper + build config) |

Notable raw signals (interpret in §7):

- **Backend language divergence**: Python's 13 files vs. Java's 26 files — Java's
  extra count reflects verbosity (type declarations, class per interface pattern)
  and the Maven project structure (separate `main/` and `test/` source trees), not
  necessarily more logic.
- **Total code volume**: Python/Vue shipped 8,135 LOC; Java/React shipped 6,481
  — *fewer* lines in Java despite more files, suggesting more compact modules or
  fewer utilities in the Java version.
- **Frontend parity**: Vue and React have similar file counts (27 vs. 32), suggesting
  comparable component granularity.
- **Test strategy divergence**: Python has 8 test files; Java has 19 (split between
  backend unit tests, integration tests, and smoke checks). Java's test structure is
  more granular (per controller, per repository, per validator).

---

## 7. Qualitative Analysis

### 7.1 Architecture & Structure

#### Python + Flask + Vue + SQLite

- **Backend**: Flask application with:
  - `backend/app.py` — main entry point, route registration
  - `backend/database.py` — SQLite initialization, schema setup
  - `backend/models.py` — Question, Quiz, ExamAttempt ORM models (SQLAlchemy)
  - `backend/repositories/` — data-access layer (`question_repo.py`, `quiz_repo.py`, `exam_repo.py`)
  - `backend/validators.py` — question/quiz validation logic
  - `backend/routes/` — REST handlers for questions, quizzes, exams
  - 13 Python files total; lightweight framework, minimal boilerplate

- **Frontend**: Vue 3 + TypeScript SPA with:
  - `frontend/src/App.vue` — root component (mounted at `#app`)
  - `frontend/src/pages/` — 6 page components (QuestionsPage, QuizListPage, etc.)
  - `frontend/src/components/` — reusable components (QuestionEditor, ConfirmDialog, etc.)
  - `frontend/src/api/` — API client (`questions.ts`, `quizzes.ts`, `exams.ts`)
  - `frontend/src/types.ts` — shared TypeScript types
  - Vue-focused: single-file components (`.vue`), computed properties, v-if/v-for reactivity
  - 27 files total; idiomatic Vue 3 Composition API structure

- **Database**: SQLite with:
  - `PRAGMA user_version` for schema versioning (migrations on startup)
  - Single `database.py` module that auto-creates the schema
  - Schema contracts: `questions.correct` (0-based index), no foreign keys (implicit)
  - File-based: `data/quiz_bank.db` (test data included in repo)

#### Java + Spring Boot + React + PostgreSQL

- **Backend**: Spring Boot 3 application with:
  - `backend/src/main/java/com/quizbank/QuizBankApplication.java` — main entry point
  - `backend/src/main/java/com/quizbank/config/WebConfig.java` — Spring MVC + static resource serving
  - `backend/src/main/java/com/quizbank/web/` — REST controllers (QuestionController, QuizController, ExamController)
  - `backend/src/main/java/com/quizbank/question/` — Question model, validator, repository
  - `backend/src/main/java/com/quizbank/quiz/` — Quiz model, validator, repository
  - `backend/src/main/java/com/quizbank/exam/` — ExamAttempt model, repository
  - `backend/src/main/java/com/quizbank/web/` — API exception handler, custom exceptions
  - 26 Java files total (split across multiple logical packages); verbose typing, explicit interfaces
  - Uses JdbcTemplate for data access (not ORM), spring-boot-starter-web for HTTP

- **Frontend**: React 18 + TypeScript SPA with:
  - `frontend/src/App.tsx` — root component (mounted at `#root`), page state machine
  - `frontend/src/pages/` — 6 page components (QuestionsPage, ExamTakingPage, etc.)
  - `frontend/src/components/` — reusable components (AppShell, QuestionEditorModal, EmptyState, etc.)
  - `frontend/src/api/` — API client modules (`questions.ts`, `quizzes.ts`, `exams.ts`)
  - `frontend/src/types.ts` — shared TypeScript types
  - React-focused: functional components + hooks (useState, useEffect, useContext), JSX, inline styles
  - 32 files total; slightly more modular than Vue (separate component files + styles)
  - Vite build system (modern, fast dev server)

- **Database**: PostgreSQL 16+ with Flyway migrations:
  - `backend/src/main/resources/db/migration/V1__baseline.sql` → `V4__create_exam_attempts.sql`
  - Schema versioning via Flyway (automatic on Spring Boot startup)
  - Schema contracts: `questions.option_a..d` columns (explicit), `correct` (0-based index)
  - Service-based: PostgreSQL must be running locally (Docker or native install)
  - Flyway manages all DDL; no app code for schema creation

### 7.2 Data Model & Schema Versioning

| Aspect                     | Python + Vue + SQLite                                    | Java + React + PostgreSQL                                |
| -------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| Schema versioning strategy | `PRAGMA user_version` (SQLite)                           | Flyway migrations (SQL scripts)                          |
| Migration tracking         | Version number in DB pragma                              | `flyway_schema_history` table                            |
| Answer column name         | `questions.correct`                                      | `questions.correct`                                      |
| Option columns             | `option_a`, `option_b`, `option_c`, `option_d`           | `option_a`, `option_b`, `option_c`, `option_d`           |
| Answer type                | 0-based index (0=A, 1=B, 2=C, 3=D)                       | 0-based index (0=A, 1=B, 2=C, 3=D)                       |
| Foreign keys               | Implicit (no enforcement in SQLite)                      | Explicit (`FOREIGN KEY REFERENCES`)                      |
| Difficulty default         | `'Medium'` string                                        | `'Medium'` string                                        |
| Exam answer tracking       | `exam_answers(attempt_id, question_id, selected_option)` | `exam_answers(id, attempt_id, question_id, user_answer)` |

**Shared schema compatibility**: Both branches use the same **logical** table/column names
and types, enabling cross-branch seed data import (see `.devflow/memory.md` for the plan).

### 7.3 Test Strategy

#### Python + Vue + SQLite

- **Backend**: 8 test files with pytest
  - `test_question_routes.py`, `test_quiz_routes.py`, `test_exam_routes.py` — API endpoint tests
  - `test_question_validators.py`, `test_quiz_validators.py` — validation logic tests
  - `test_repositories.py` — data-access layer tests (against SQLite fixtures)
  - Uses `@pytest.fixture` for test isolation, mocks Flask client for HTTP testing
  - Full end-to-end exam flow tested (create attempt → save answer → submit → score)

- **Frontend**: No Jest/Vitest unit tests in the Python/Vue branch — only manual
  browser verification noted in evidence files.

- **Coverage**: All 87 acceptance criteria marked PASS; smoke tests passed in browser.

#### Java + React + PostgreSQL

- **Backend**: 19 test files with JUnit 5 + Spring Boot Test
  - `QuestionRepositoryTest.java` — repository layer (JdbcTemplate queries)
  - `QuestionValidatorTest.java` — validation logic
  - `QuestionApiTest.java`, `QuizApiTest.java`, `ExamApiTest.java` — controller layer (@WebMvcTest)
  - `ReleaseSmokeTest.java` — integration test (starts full Spring context, hits running app over HTTP)
  - Structured per layer: unit tests for repositories/validators, integration tests for APIs
  - Full end-to-end exam flow tested (attempt creation, answer persistence, scoring, 409 on re-submit)

- **Frontend**: `frontend/src/questionsFilter.test.ts` — vitest unit test for the
  search/filter utility; no DOM component tests.

- **Coverage**: All 87 acceptance criteria marked PASS; smoke tests passed in browser
  (React app rendered, all three versions functional, all flows completed).

### 7.4 Correctness & Behavior Parity (this session)

Both stacks were **built and verified in-browser** this session:

- **Python + Vue + SQLite**:
  - ✅ Question Bank: add, edit, delete, search fully functional
  - ✅ Quiz Builder: create, reorder, preview, save fully functional
  - ✅ Online Exam: start, answer, submit, review fully functional
  - ✅ Data persistence across restarts verified
  - ✅ All pytest tests green (8 files)

- **Java + Spring Boot + React + PostgreSQL**:
  - ✅ Question Bank: add, edit, delete, search fully functional
  - ✅ Quiz Builder: create, reorder, preview, save fully functional
  - ✅ Online Exam: start, answer, submit, review fully functional
  - ✅ Data persistence across restarts verified (PostgreSQL)
  - ✅ All JUnit tests green (19 files)
  - ✅ Flyway migrations automatic on startup (no manual schema setup)

**No hidden bugs or runtime failures.** Both implementations honored the spec.

### 7.5 Spec Adherence & Scope

Both stacks completed all 18 tasks (o01/t01 → o03/t06) as specified:

| Version | Tasks             | Python/Vue | Java/React |
| ------- | ----------------- | ---------- | ---------- |
| V1      | o01/t01 → o01/t06 | ✅ PASS    | ✅ PASS    |
| V2      | o02/t01 → o02/t06 | ✅ PASS    | ✅ PASS    |
| V3      | o03/t01 → o03/t06 | ✅ PASS    | ✅ PASS    |

No scope creep, no features added beyond the spec. Both branches:

- Delivered 87 acceptance criteria (same count, same text, all verified PASS)
- Built the same three user-visible flows (Question Bank, Quiz Builder, Online Exam)
- Excluded out-of-scope features (authentication, multi-user, cloud deployment)

### 7.6 Setup Complexity & Local-Dev Ergonomics

| Aspect                    | Python + Vue + SQLite        | Java + React + PostgreSQL                                        |
| ------------------------- | ---------------------------- | ---------------------------------------------------------------- |
| **Backend prerequisite**  | Python 3.x, pip              | JDK 21+                                                          |
| **Frontend prerequisite** | Node.js, npm                 | Node.js, npm (same)                                              |
| **Database prerequisite** | None (file-based)            | PostgreSQL 16+ service (Docker or native)                        |
| **Setup time**            | ~5 minutes (npm install)     | ~15 minutes (JDK + PostgreSQL + npm)                             |
| **Startup command**       | `py -m backend`              | `npm run build && ./mvnw spring-boot:run`                        |
| **Schema initialization** | Automatic (Flask on startup) | Automatic (Flyway on Spring Boot startup)                        |
| **Schema reset**          | Delete `data/quiz_bank.db`   | `DROP DATABASE quiz_bank; CREATE DATABASE quiz_bank OWNER quiz;` |
| **Database visibility**   | Single file in repo          | Running service (external to repo)                               |

**Trade-off analysis**:

- **Python/Vue is simpler to bootstrap**: No database service needed; a single `py -m backend`
  command starts the app. Lower barrier to entry for students / local experimentation.
- **Java/React requires more infrastructure**: PostgreSQL must be installed and running.
  Higher barrier to entry, but more production-grade (PostgreSQL is industry-standard;
  SQLite is a demo database). Better for demonstrating real-world stack choices.

---

## 8. Summary / Conclusions

### 8.1 Code Metrics

- **Both stacks are similar in total volume** (8.1k vs 6.5k LOC in code areas) —
  size alone does not explain the architectural differences.
- **Java is more verbose** (26 backend files vs. 13 Python), reflecting Java's
  syntax and project layout conventions (package structure, separate src/test/
  trees). The code is not longer, just spread across more files.
- **Frontend granularity is similar** (27 Vue files vs. 32 React files) — both
  stacks favored component-based modularity.

### 8.2 Architecture & Design

- **Python/Vue**: lightweight, convention-over-configuration approach; SQLAlchemy ORM
  handles queries; single `database.py` module bootstraps the schema. Fewer explicit
  interfaces, more implicit contracts.
- **Java/React**: explicit, layered architecture (web → repositories → database);
  JdbcTemplate for data access (not ORM); 4 Flyway migrations for schema versioning.
  More interfaces, more separation of concerns.

### 8.3 Database & Infrastructure

- **SQLite (Python/Vue)**: zero-configuration, file-based, shipped with test data in repo.
  Best for local dev / lightweight demos; breaks at scale.
- **PostgreSQL (Java/React)**: production-grade, requires a service, enables real-world
  database concepts (foreign keys, complex queries, indexing). Steeper learning curve,
  but more relevant to industry practice.

### 8.4 Tests

- **Python**: 8 unit/integration test files; no frontend tests.
- **Java**: 19 test files (more granular, per-layer structure); 1 minimal vitest utility.

Both passed all tests; both verified in-browser. Test granularity is a style choice,
not a correctness indicator.

### 8.5 Spec Adherence

**Both stacks honored the specification exactly.** All 18 tasks completed, 87 acceptance
criteria verified. No scope creep in either direction.

### 8.6 Method Takeaway

The refactor experiment validates DevFlow's **stack-agnostic specification model**:

1. A single set of artifacts (intent, objectives, tasks) can drive multiple
   implementations without modification.
2. Different stacks can make different architectural choices (ORM vs. JDBC, file-based
   vs. service-based database) while keeping the same API contract and UI behavior.
3. Cross-branch schema compatibility is achievable if **logical** table/column names
   are preserved (even if **physical** implementation details differ).

Future branches can reuse this experiment's lessons:

- The schema contract (questions, quizzes, quiz_questions, exam_attempts, exam_answers
  with consistent column names) is now proven portable.
- The artifact-first workflow (alignment before code) catches ambiguities early and
  enables confident multi-stack builds.
- DevFlow is **not** tied to a single language, framework, or database — it's a
  specification methodology.

---

## 9. Method Notes & Caveats

- File counts and LOC are **proxies**, not quality scores — a smaller build is not
  automatically worse.
- Metrics are from the implementation commits (before post-impl documentation and ADR
  additions). Re-run §5's commands to verify against current branch tips.
- Both stacks were implemented by AI coding assistants (Claude Code + Cursor for
  Python/Vue; Claude Code for Java/React). Tool variation is **not** the primary
  comparison variable — stack choice is.
- Behavior parity was verified **in-browser** in this session; both apps are
  production-ready for demo purposes.

---

## 10. Artifacts

Refer to the following for detailed evidence:

| Artifact               | Location                                          | Purpose                              |
| ---------------------- | ------------------------------------------------- | ------------------------------------ |
| Python/Vue ACR         | `.devflow/evidence/python_acr.md`                 | Merged acceptance criteria (87 rows) |
| Java/React ACR         | `.devflow/evidence/java_acr.md`                   | Merged acceptance criteria (87 rows) |
| Python/Vue screenshots | `screenshots/python_*.png`                        | Browser verification (9 images)      |
| Java/React screenshots | `screenshots/java_*.png`                          | Browser verification (9 images)      |
| Python/Vue ADR         | `docs/tech-stack.md` (Python/Vue)                 | Stack decision record                |
| Java/React ADR         | `docs/ADR-01-java-react-postgresql-full-stack.md` | Stack decision record                |

---

**Version:** 2.0  
**Date:** 2026-07-13  
**Verified stacks:** Python + Flask + Vue 3 + SQLite, Java 21 + Spring Boot 3 + React 18 + PostgreSQL  
**Coverage:** Both branches built and verified end-to-end (all three product versions)
