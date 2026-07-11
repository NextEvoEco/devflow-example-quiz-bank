# Tech Stack Refactor Guide

## Purpose

This document is the base checklist for creating `refactor/*` branches that change the implementation technology stack.

Use it before and during a stack migration such as:

- Python -> Java
- plain JavaScript -> TypeScript
- Flask -> Spring Boot
- SQLite -> PostgreSQL
- static frontend -> framework-based frontend

This guide provides no per-file checklist for `.devflow/context/*.md`.
Those files are still part of a stack refactor (see §8 step 5) — handle them once the
branch-specific refactor direction is confirmed, typically driven by the branch intent.

---

## 1. What This Guide Covers

When the tech stack changes, check and update:

- `.devflow/interview/`
- `.devflow/objective/`
- `.devflow/tasks/`
- `README.md`
- `docs/`
- root-level tooling files such as `.gitignore`, dependency manifests, build scripts, and startup commands
- source-code directory assumptions referenced by prompts or workflow artifacts

This guide is not the migration plan itself.
It is the artifact-alignment checklist that keeps DevFlow instructions and prompts consistent with the chosen refactor branch.

---

## 2. Refactor Branch Rule

For each tech-stack refactor, create a dedicated branch such as:

- `refactor/java-backend`
- `refactor/typescript-frontend`
- `refactor/java-typescript`
- `refactor/postgresql`

Do not try to maintain one generic "future stack" state across all artifacts.
Each branch should describe only its own chosen stack.

---

## 3. Checklist By Area

### A. `.devflow/interview/`

Goal:
- identify where old stack decisions were explicitly confirmed by the user

What to check:
- questions that asked the user to choose backend language
- questions that asked the user to choose frontend stack
- questions that asked the user to choose persistence technology
- questions that asked how the app is started locally

What usually needs updating:
- add a branch-specific note that the original confirmed stack has been superseded by this refactor branch
- if the interview is being used as current truth, update the answer summary to the new stack

Current known hotspot:
- `.devflow/interview/i01-question-bank.md`

Examples of old decisions currently written there:
- plain HTML/CSS/JavaScript
- SQLite
- Python
- local web app started by a Python server

---

### B. `.devflow/objective/`

Goal:
- make sure objectives describe the current implementation platform and success criteria accurately

What to check:
- `Tech Stack` rows
- `Platform` rows
- startup/runtime wording
- persistence wording
- success criteria that name old technologies directly

What usually needs updating:
- replace old stack names with the new branch stack
- update "started by Python server" style wording
- update "stored in SQLite" wording if database changes
- keep product scope unchanged unless the refactor branch intentionally changes product scope

Current known hotspots:
- `.devflow/objective/o01-question-bank-v1.md`
- `.devflow/objective/o02-quiz-builder-v1.md`
- `.devflow/objective/o03-online-exam-v1.md`

---

### C. `.devflow/tasks/`

Goal:
- remove stale implementation instructions that point to the old stack, old commands, or old file layout

What to check in every task:
- language/framework assumptions
- startup commands
- test commands
- file paths
- module names
- database and migration assumptions
- frontend structure assumptions

What usually needs updating:
- `py -m backend`
- `py -m pytest tests -v`
- `requirements.txt`
- `backend/app.py`
- `backend/database.py`
- `backend/models.py`
- `frontend/index.html`
- `frontend/js/app.js`
- `frontend/css/app.css`
- "Flask blueprint"
- "SQLite migration"
- "plain JavaScript frontend"

Current high-priority task groups:

- `o01/t01-bootstrap-local-web-app`
  - bootstrap language/runtime/server assumptions
- `o01/t02-build-question-storage-and-validation`
  - persistence and validation implementation assumptions
- `o01/t03-implement-question-bank-api`
  - API-layer stack assumptions
- `o02/t01-quiz-db-schema`
  - DB schema and migration assumptions
- `o02/t02-quiz-api`
  - route/controller/repository assumptions
- `o03/t01-add-exam-attempts-schema`
  - repository/model/migration path assumptions
- `o03/t02-implement-exam-api`
  - backend routing pattern assumptions
- `o03/t06-add-tests-and-release-verification`
  - release commands and verification commands

Important note:
- some existing task files already contain stale path references even before a stack migration
- do not blindly preserve outdated file names if the live repo or target refactor layout differs
- task files inherited from the base carry `Status: verified` and checked acceptance boxes
  from the original build; on a refactor branch, reset them (e.g. `Status: ready`, uncheck
  the boxes) so a fresh AI session does not treat unstarted work as already done — this
  exact trap was hit during the rebuild experiment (see the tool branches' `memory.md`)

---

### D. `README.md`

Goal:
- keep the public bootstrap instructions aligned with the branch stack

What to check:
- version status summary
- install commands
- startup commands
- test commands
- references to dependency managers
- references to runtime names

What usually needs updating:
- `pip` / `requirements.txt`
- `py -m backend`
- `py -m pytest`
- Python/Flask/SQLite wording
- any stack summary in the project status section

---

### E. `docs/`

Goal:
- keep all release-verification and getting-started instructions runnable on the target branch

What to check:
- startup instructions
- install instructions
- test instructions
- data-reset instructions
- references to local DB file names
- wording that says a stack is planned, disabled, or not yet implemented

Files likely to need review:
- `docs/getting-started.md`
- any release/verification guides present on the branch — names vary by branch history
  (e.g. `v1-*-release.md`, `v*-verification.md`); on `refactor/base` only
  `docs/getting-started.md` exists, so a stack branch typically creates its own
  verification docs rather than editing inherited ones

What usually needs updating:
- startup command examples
- test command examples
- dependency manager instructions
- DB reset instructions
- "current version" or "planned version" wording if the branch changes release framing

---

### F. Root Tooling Files

Goal:
- keep repo-level tooling consistent with the branch stack

What to check:
- `.gitignore`
- `requirements.txt`
- future `package.json`, `pom.xml`, `build.gradle`, `tsconfig.json`, `Dockerfile`, CI files, or wrapper scripts

What usually needs updating:
- ignore rules for new build outputs
- old dependency manifests that no longer apply
- startup/test commands embedded in scripts

---

## 4. Search Keywords

Before editing, run searches for these terms across DevFlow and docs artifacts:

- `Python`
- `Flask`
- `SQLite`
- `plain HTML/CSS/JavaScript`
- `JavaScript`
- `pytest`
- `py -m pytest`
- `py -m backend`
- `requirements.txt`
- `backend/`
- `frontend/`
- `app.py`
- `database.py`
- `models.py`

Then add branch-specific keywords:

- `Java`
- `Spring`
- `Gradle`
- `Maven`
- `TypeScript`
- `Node`
- `pnpm`
- `npm`
- `PostgreSQL`
- `MySQL`

---

## 5. What Usually Does Not Need Immediate Change

These items often remain valid unless the refactor changes product behavior:

- `.devflow/context/ui-spec.md`
- product-scope statements about Question Bank / Quiz Builder / Online Exam
- non-technical acceptance criteria describing user-facing behavior

Even so, review them if the new stack changes:

- routing model
- SPA vs multi-page architecture
- client/server rendering assumptions
- persistence behavior visible to users

---

## 6. Branch Refactor Prompt Template

Use this as the base prompt when creating a new `refactor/*` branch:

```text
Refactor this repository to the following tech stack:

- Backend:
- Frontend:
- Database:
- Build/test tooling:
- Startup command:

Rules:
- Keep product behavior and DevFlow workflow intact unless explicitly changed.
- Update implementation code, docs, and workflow artifacts to match the new stack.
- Do not update `.devflow/context/*.md` in this pass.
- Do update `.devflow/interview/`, `.devflow/objective/`, `.devflow/tasks/`, `README.md`, and `docs/` anywhere the old stack is written or implied.
- Replace stale commands, file paths, dependency-manifest references, and framework-specific wording.
- Keep acceptance criteria focused on product behavior, not on the old implementation technology.
- Preserve or replace automated tests so the new stack still has a runnable verification baseline.

Required checks:
- Search for old stack keywords before editing.
- Update startup/test/install commands.
- Update release verification docs.
- Update task files that mention old file names, frameworks, commands, or persistence assumptions.
- Summarize every artifact updated because of the stack change.
```

---

## 7. Branch-Specific Prompt Add-Ons

### Java Backend Refactor Add-On

```text
Additional branch intent:
- Replace Python/Flask backend assumptions with Java backend assumptions.
- Update all references to Python runtime, Flask, `py -m backend`, and `requirements.txt`.
- Replace backend file-path assumptions if the code moves to `src/main/java/` or similar.
```

### TypeScript Frontend Refactor Add-On

```text
Additional branch intent:
- Replace plain JavaScript assumptions with TypeScript assumptions.
- Update all references to `frontend/app.js`, "plain JavaScript", and direct JS-only wording.
- If a frontend framework is introduced, update tasks and docs that assume static HTML plus direct DOM scripting.
```

### Database Refactor Add-On

```text
Additional branch intent:
- Replace SQLite-specific wording with the new persistence technology.
- Update references to local DB files, migration assumptions, reset instructions, and startup prerequisites.
```

---

## 8. Recommended Execution Order

When running a stack-refactor branch, a safe order is **artifacts first, code second** —
the aligned markdown is what drives the implementation pass:

1. Choose the target stack and branch name (branched from `refactor/base`).
2. Record the branch intent in `.devflow/intent/`, naming the target stack and this guide.
3. Update `.devflow/interview/`, `.devflow/objective/`, and `.devflow/tasks/`
   (markdown-alignment pass only — no code yet; reset inherited task statuses, see §3.C).
4. Update `README.md` and `docs/`.
5. Update `.devflow/context/*.md` for the target stack (same pass or a follow-up one).
6. Implement the code and build tooling, driven by the aligned `context/` and `tasks/`.
7. Re-run the branch's automated checks.
8. Produce a short artifact-diff summary of what changed because of the stack refactor.

A branch intent may override this order, but steps 2–5 should complete before step 6 so the
implementing session reads a consistent spec.

---

## 9. Outcome Standard

A tech-stack refactor branch is not complete just because the code compiles.

It is complete only when:

- the implementation matches the new stack
- startup and test instructions are runnable
- DevFlow planning artifacts no longer instruct future AI to use the old stack
- release-verification docs match the branch reality
- automated checks include at least one **black-box smoke check against the running app**
  (HTTP API level, ideally also DOM level) — in the rebuild experiment, a branch with an
  all-green unit suite still shipped a broken UI that only a running-app check would catch
- if cross-stack comparison is planned, the branch preserves the shared behavior contract —
  same routes, request/response payload shapes, default port, and a documented startup
  entrypoint — so different stacks stay black-box comparable
