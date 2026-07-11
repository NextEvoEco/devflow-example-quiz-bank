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

## 2026-07-11 - Frontend Init Aborts If app.js References a Missing Element

- Type: caveat
- Scope: `frontend/app.js` and `frontend/index.html`
- Detail: `app.js` caches DOM nodes by id into an `elements` object at load, then `bindEvents()` calls `addEventListener` on many of them, and the bootstrap runs `bindEvents()` BEFORE `loadQuestions()/loadQuizzes()`. If any id referenced in `app.js` is missing from `index.html`, `getElementById` returns `null`, `bindEvents()` throws a TypeError, and the WHOLE bootstrap aborts — no event handlers bind and no `/api/*` calls fire, so the page renders static HTML with dead buttons and no data (server log shows only `/`, `/app.js`, `/styles.css`, no `/api`). This happened because `app.js` expected `back-to-exams-button` and `exam-taking-copy`, which `index.html` did not define; both were added to `index.html` to fix it. Guard rule: every id used via `getElementById` in `app.js` must exist in `index.html` (quick check: diff the id sets).
- Source: debugging "buttons do nothing" on `rebuild/codex`; the running app made no API requests.

## 2026-07-11 - Seeding Data From main's DB Needs Schema Translation

- Type: caveat
- Scope: `data/quiz_bank.db`, `backend/db.py`, cross-branch data reuse
- Detail: `data/*.db` is git-ignored on rebuild branches, but `main` committed a `data/quiz_bank.db`. That DB comes from a different implementation: its `questions` answer column is named `correct` and its `schema_migrations` already lists versions 1–4. This branch's code queries `correct_answer` and defines migrations 1–3. Copying main's DB verbatim does NOT work: because `schema_migrations` already covers 1–3, this branch's migrations are skipped, so the foreign schema (`correct` column) is reused and every query for `correct_answer` fails — the app returns empty/errors. Correct approach: build a fresh DB via this branch's `initialize_database`, then copy rows mapping `correct` → `correct_answer`. Also note main's committed DB stored EMPTY option_a–d; full option text lives in the seed markdown `fixtures/world-geography-basic-50.md` (from ancestor commit `10863f6`), matched to questions by text.
- Source: diagnosing "DB has data but the exam screen shows nothing" on `rebuild/codex`.

## 2026-07-08 - Bootstrap State Corrected

- Type: handoff
- Scope: DevFlow runtime state and repository context
- Detail: The repo artifacts previously described a fully implemented V1-V3 app, but the live workspace only contained DevFlow/docs files. The bootstrap task is the first code implementation now present under backend/frontend/tests.
- Source: direct repository inspection during execution of `o01/t01`
