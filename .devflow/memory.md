# Execution Memory

This file stores durable, non-obvious facts that should survive across sessions.

Use it for information that is important to remember but does not belong in `status.md`, a task file, or an evidence file.

---

## When To Write Here

Add an entry when you discover:

- a confirmed constraint that is easy to forget
- a recurring caveat
- a repository behavior not obvious from filenames alone
- a handoff note useful to future AI sessions

Do not use this file for:

- current task progress
- general project overview that belongs in context files
- implementation evidence that belongs in evidence artifacts

---

## Entry Format

Add new entries at the top using this structure:

```text
## YYYY-MM-DD - Short Title

- Type: constraint | caveat | handoff | decision | other
- Scope: {what part of the project this affects}
- Detail: {the durable fact}
- Source: {how this was learned}
```

---

## Entries

## 2026-06-28 - Quiz Builder V1 Release Verification

- Type: handoff
- Scope: release
- Detail: Run `py -m pytest tests/ -v` and follow `docs/o02-verification.md` before demonstrating Quiz Builder V1. All `o02/t01` through `o02/t06` tasks are complete. Quiz Builder nav is enabled; Online Exam remains disabled.
- Source: `o02/t06` implementation and verification

## 2026-06-28 - Quiz Builder Hash Init

- Type: caveat
- Scope: frontend navigation
- Detail: `quiz-builder.js` must load builder data on init when the URL hash is `#quizCreate` or `#quizCreate/<id>`; otherwise a direct hash load before module init can leave the builder panels empty.
- Source: `o02/t06` manual verification

## 2026-06-28 - Manual Geography Demo Fixture

- Type: handoff
- Scope: demo content
- Detail: The app still starts with an empty Question Bank by default. The file `fixtures/world-geography-basic-50.md` contains about 50 English world geography questions prepared for manual input and demo use; it is not auto-imported or preloaded.
- Source: repository fixture creation and current V1 scope

## 2026-06-28 - Quiz API Endpoints

- Type: handoff
- Scope: backend API
- Detail: Quiz routes live under `/api/quizzes`. Create/update payloads use `name` and ordered `questionIds`; detail responses include full `questions` objects for preview support.
- Source: `o02/t02` implementation and verification

## 2026-06-28 - Quiz Schema Migration v3

- Type: handoff
- Scope: database
- Detail: Migration v3 adds `quizzes` and `quiz_questions` tables. `quiz_questions` stores ordered question references via `position` and foreign keys to `quizzes.id` and `questions.id`.
- Source: `o02/t01` implementation and verification

## 2026-06-28 - V1 Release Verification

- Type: handoff
- Scope: release
- Detail: Run `py -m pytest` and follow `docs/v1-verification.md` before demonstrating Question Bank V1. All `o01/t01` through `o01/t06` tasks are complete.
- Source: `o01/t06` implementation and verification

## 2026-06-28 - Question Bank API Endpoints

- Type: handoff
- Scope: backend API
- Detail: Question Bank HTTP routes live under `/api/questions` with optional `?q=` search, plus item routes at `/api/questions/<id>` for read, update, and delete.
- Source: `o01/t03` implementation and verification

## 2026-06-28 - Local App Startup Command

- Type: handoff
- Scope: application bootstrap
- Detail: Start the Quiz Bank local app from the repository root with `py -m backend`. The server listens on `http://127.0.0.1:5000` and creates `data/quiz_bank.db` automatically on first run.
- Source: `o01/t01` implementation and verification
