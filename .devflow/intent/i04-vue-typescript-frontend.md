# Intent: Vue + TypeScript Frontend Refactor

**ID:** i04-vue-typescript-frontend
**Date:** 2026-07-11
**Status:** clarified
**Source:** user prompt

---

## 1. Original Request

> What did the user ask for?

```text
You are on branch refactor/python-vue-sqlite.

Read docs/tech-stack.md first — it is the checklist that drives this pass.

Target tech stack for this branch:
- Backend: Python + Flask (unchanged)
- Frontend: Vue 3 + TypeScript + Vite (replaces plain HTML/CSS/JavaScript)
- Database: SQLite (unchanged)
- Build/test tooling: pip + pytest for backend; npm + vitest for frontend
- Startup: py -m backend serves the API and the built frontend (dist/)

Do this pass in order (tech-stack.md §8 steps 2–5), markdown only — NO application code:

1. Record the branch intent as .devflow/intent/i04-vue-typescript-frontend.md using
   .devflow/templates/intent-template.md: this branch refactors the frontend layer to
   Vue 3 + TypeScript while keeping Python/Flask and SQLite, driven by docs/tech-stack.md.
2. Update .devflow/interview/, .devflow/objective/, and .devflow/tasks/ per tech-stack.md
   §3.A–C and the §7 "TypeScript Frontend Refactor Add-On": replace plain-JS/static-HTML
   assumptions with Vue 3 + TypeScript + Vite assumptions. Keep product behavior and
   acceptance criteria unchanged — they describe user-facing behavior, not the stack.
3. Reset inherited task states (§3.C): Status: verified → ready, uncheck acceptance boxes.
4. Update README.md and docs/ (§3.D–E): install/startup/test commands for the two-part
   toolchain (pip + npm).
5. Update .devflow/context/*.md for this stack, including ui-spec.md where it assumes a
   single static index.html with per-page sections — this branch becomes a Vite-built SPA.
6. Run the §4 keyword searches before and after editing; finish with an artifact-diff
   summary listing every file changed and why.

Preserve the behavior contract: same API routes and JSON shapes, same port 5000,
same user-visible flows (Question Bank / Quiz Builder / Online Exam).
Update .devflow/status.md to point at this alignment work when done. Do not commit.
```

---

## 2. Motivation

> Why does this request matter?

This branch is part of the tech-stack refactor experiment: proving that DevFlow
artifacts can drive a stack migration on a branch, with each `refactor/*` branch
describing only its own stack. This first branch changes exactly one layer (the
frontend) so the migration process itself can be calibrated before larger jumps
(e.g. Java backend, PostgreSQL) are attempted on later branches.

---

## 3. Known Constraints

> List any constraints already known before interview or planning.

- Product behavior and DevFlow workflow stay intact; only the frontend stack changes.
- Preserve the behavior contract: same API routes and JSON shapes, same port 5000,
  same user-visible flows (Question Bank / Quiz Builder / Online Exam).
- Backend (Python/Flask), persistence (SQLite), and backend testing (pytest) are
  explicitly out of scope for this refactor.
- The original stack decisions recorded in `.devflow/interview/i01-question-bank.md`
  (plain HTML/CSS/JavaScript frontend) are superseded on this branch only.
- Follow `docs/tech-stack.md`: artifacts first, code second (§8); reset inherited task
  states (§3.C); completion bar is §9 including a black-box smoke check.

---

## 4. Unknowns

> What still needs clarification before objective definition?

- None blocking. Component structure and build integration details are decided during
  the implementation pass within the constraints above.

---

## 5. Notes

The markdown-alignment pass for this intent updates: `.devflow/interview/i01`,
`.devflow/objective/o01–o03`, `.devflow/tasks/o01–o03`, `README.md`, `docs/`, and
`.devflow/context/*.md` (including `ui-spec.md`, since the static
one-HTML-plus-page-sections shell becomes a Vite-built Vue SPA).
