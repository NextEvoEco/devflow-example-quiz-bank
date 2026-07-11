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

## 2026-07-11 - This Is the Cursor Rebuild Branch

- Type: handoff
- Scope: whole repository; the rebuild comparison experiment
- Detail: This branch (`rebuild/cursor`) is one of several that reconstruct the same Quiz Bank app from the same DevFlow artifacts, each with a different AI tool (see the *Rebuild Comparison Experiment* section in `README.md` and `docs/rebuild-comparison.md`). Rebuild only from this branch's artifacts; do not copy the sibling branches (`rebuild/code`, `rebuild/codex`). Tool outputs use a `cursor_` prefix (`.devflow/evidence/cursor_acr.md`, `screenshots/cursor_*.png`). Schema note: this build stores the answer key in a `correct` column (same as `rebuild/code`; `rebuild/codex` renamed it to `correct_answer`), and versions the schema via a `schema_migrations` table. `data/*.db` is git-ignored, so a working-tree DB does not travel with the branch; a DB borrowed from another branch only fits if its `questions` schema matches (`correct` here).
- Source: rebuild-experiment alignment pass on 2026-07-11.

## 2026-07-08 - Shell execution may fail silently

- Type: caveat
- Scope: local verification during task execution
- Detail: In this session, shell and shell-subagent command execution stopped returning stdout/stderr and exit status, even for trivial commands. Do not mark work as verified unless command execution is healthy again.
- Source: o01/t03 verification attempts with `py -m pytest -v`, `python -m pytest -v`, `cmd /c`, and `echo`

## 2026-07-08 - Question IDs use SQLite autoincrement

- Type: decision
- Scope: Question Bank persistence (`backend/question_repository.py`)
- Detail: Question `id` values are SQLite INTEGER PRIMARY KEY AUTOINCREMENT, not `Date.now()` as described in the UI-spec prototype. API/UI consumers should treat IDs as opaque integers assigned by the database.
- Source: o01/t02 implementation against ui-spec Question data fields

## 2026-07-08 - Context files ahead of live code

- Type: caveat
- Scope: `.devflow/context/*` vs `backend/` / `frontend/` / `tests/`
- Detail: At o01/t01 execution, context files described a complete V1–V3 Quiz Bank implementation, and task files were marked verified, but application source directories were missing. Trust live code and current evidence over stale context claims. After t01, only the local Flask shell + SQLite bootstrap exists; Question Bank CRUD is not implemented yet.
- Source: Observed empty `backend/`, `frontend/`, `tests/` while executing o01/t01; verified foundation rebuilt and tested.

## 2026-07-08 - Local app startup command

- Type: handoff
- Scope: local development
- Detail: Start the app from repo root with `py -m backend` after `pip install -r requirements.txt`. Server listens on `http://127.0.0.1:5000/`. SQLite file is created at `data/quiz_bank.db` on first start. Runtime `data/` is gitignored.
- Source: o01/t01 bootstrap verification
