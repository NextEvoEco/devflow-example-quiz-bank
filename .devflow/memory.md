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

## 2026-07-12 - Seed Imported Into PostgreSQL; SQLite Remains Optional Source

- Type: handoff
- Scope: `data/quiz_bank.db`, `scripts/import_seed_from_sqlite.py`, PostgreSQL `quiz_bank`
- Detail: Demo seed (50 questions, 3 quizzes) was imported successfully via
  `python scripts/import_seed_from_sqlite.py` against Docker `quiz-bank-pg`.
  Verified `GET /api/questions` returns 50 items and quizzes list shows 3 quizzes.
  Import steps are documented in `docs/installation-guide.md` §8. The SQLite file
  may still be kept as a regenerable seed source; runtime never opens it.
- Source: implementation pass completion on 2026-07-12

## 2026-07-12 - data/quiz_bank.db Is a Temporary Seed Source, Not This Branch's Database

- Type: handoff
- Scope: `data/quiz_bank.db`, PostgreSQL seed data, end of the implementation pass
- Detail: This branch persists to PostgreSQL (database `quiz_bank`, schema created by
  Flyway) — it does NOT use SQLite at runtime. The committed `data/quiz_bank.db` is
  intentionally kept as the SEED SOURCE only: it holds the shared demo dataset
  (50 world-geography questions with full option text, 3 quizzes, quiz_questions
  links) in the same logical schema as the Flyway target (`questions.option_a..option_d`,
  `correct`, `difficulty`, ...). Plan agreed with the user: after the implementation
  pass completes and the schema exists in PostgreSQL, import this data into PostgreSQL
  (document the import steps in `docs/installation-guide.md` §8), verify the app serves
  it, then DELETE `data/quiz_bank.db` from the branch in a follow-up commit. Do not
  wire any runtime code to the SQLite file.
- Source: user decision on 2026-07-12 during the alignment pass, recorded so the
  implementation session (possibly a different tool) inherits the plan.
