# Rebuild Comparison

> Cross-tool analysis of the Quiz Bank rebuild experiment.
>
> This document is **branch-neutral**: it compares the results of every `rebuild/*`
> tool branch. It is intended to live on a dedicated comparison branch (e.g.
> `rebuild/compare`) or on `main`, **not** inside any single tool branch — the
> comparison must not favor or be authored from one competitor's perspective.
>
> **Placement:** this is the canonical copy on `rebuild/compare` (forked from `rebuild/base`).
>
> **Coverage note:** in the latest pass, `rebuild/code` and `rebuild/codex` were examined
> in depth (built / debugged); `rebuild/cursor` was compared structurally only (not run).
> Findings are scoped accordingly.

---

## 1. Purpose

The experiment answers one question:

> **Given the same DevFlow specification, how differently do AI coding tools rebuild
> the same application?**

Every tool receives the identical, code-free DevFlow artifacts (intent, interview,
objective, tasks) and must reconstruct the Quiz Bank application from them alone.
Differences between the branches are therefore attributable to the tool/model, not to
differing requirements.

---

## 2. Shared Baseline

| Item                 | Value                                                                               |
| -------------------- | ----------------------------------------------------------------------------------- |
| Baseline branch      | `rebuild/base`                                                                      |
| Baseline commit      | `c105cbd`                                                                           |
| Baseline contents    | DevFlow artifacts only — **no application code**                                    |
| Frozen specification | `.devflow/intent/`, `.devflow/interview/`, `.devflow/objective/`, `.devflow/tasks/` |

Each tool branch is a single implementation commit on top of this baseline.

---

## 3. Branch ↔ Tool Map

| Branch           | Tool        | Model                     | Impl commit (current tip) |
| ---------------- | ----------- | ------------------------- | ------------------------- |
| `rebuild/base`   | —           | —                         | `c105cbd`                 |
| `rebuild/code`   | Claude Code | Claude Opus 4.8           | `985ab65`                 |
| `rebuild/codex`  | Codex       | _(unspecified)_           | `c0639d9`                 |
| `rebuild/cursor` | Cursor      | _(unspecified)_           | `0cec980`                 |

Notes:

- Commit co-authors were removed on all tool branches, so the model is **not** recorded in
  commit metadata — identify the tool by branch. Claude Code's model (Opus 4.8) is known
  from this session; Codex's and Cursor's underlying models are unconfirmed.
- Each current tip folds in this session's doc-alignment, `*_acr.md`, and `screenshots/*`
  on top of the pure implementation. The §6 **code-area** metrics were taken from the clean
  implementation and remain representative of tool output; re-running §5's *file-count*
  command against a current tip will read higher because of those non-code additions.

---

## 4. Naming Convention

Tool-specific outputs are prefixed with the tool's short name so results from different
branches never collide when gathered together:

| Prefix    | Branch           | Examples                                                    |
| --------- | ---------------- | ----------------------------------------------------------- |
| `code_`   | `rebuild/code`   | `.devflow/evidence/code_acr.md`, `screenshots/code_*.png`   |
| `codex_`  | `rebuild/codex`  | `.devflow/evidence/codex_acr.md`, `screenshots/codex_*.png` |
| `cursor_` | `rebuild/cursor` | `.devflow/evidence/cursor_acr.md`, `screenshots/cursor_*.png` |

Per-tool artifacts (`*_acr.md`, `screenshots/*_*.png`) **stay on their own tool branch**.
This comparison branch only *aggregates or references* them.

---

## 5. Comparison Methodology

How to reproduce each measurement:

```bash
# Files a tool added on top of the shared baseline (excluding DevFlow artifacts)
git diff --name-only rebuild/base rebuild/<tool> | grep -v '^.devflow/'

# Code volume (application areas only)
git diff --shortstat rebuild/base rebuild/<tool> -- backend frontend tests

# Test functions
git grep -h -E "def test_" rebuild/<tool> -- 'tests/*.py' | wc -l

# Structural shape
git ls-tree -r --name-only rebuild/<tool> -- backend/ | grep '\.py$'
git ls-tree -r --name-only rebuild/<tool> -- frontend/ | grep '\.js$'

# Full side-by-side of two tools
git diff rebuild/<toolA> rebuild/<toolB> -- backend frontend tests
```

Dimensions worth comparing:

- **Structure** — module granularity, file layout, separation of concerns
- **Volume** — lines of code, file count (proxy, not a quality score)
- **Test coverage** — number and shape of tests, what they exercise
- **Spec adherence** — did each task boundary get honored; any scope drift
- **Correctness** — do all suites pass; behavior parity in the browser
- **Idiom / readability** — naming, comments, error handling
- **Extras** — anything a tool added beyond the tasks (seed data, docs, tooling)

---

## 6. Quantitative Results

Measured against `rebuild/base` (baseline has no code), from the clean implementation
(before this session's doc-alignment / `screenshots/` / `*_acr.md` additions — see §3 notes).

| Metric                                      | Claude Code | Codex | Cursor |
| ------------------------------------------- | ----------- | ----- | ------ |
| Files added (excl. `.devflow/`)             | 49          | 38    | 45     |
| Code files changed (backend/frontend/tests) | 42          | 32    | 38     |
| Insertions in code areas                    | 5,540       | 5,123 | 5,966  |
| Backend `.py` files                         | 15          | 10    | 15     |
| Frontend `.js` files                        | 7           | 1     | 2      |
| Test files                                  | 18          | 19    | 19     |
| Test functions (`def test_`)                | 139         | 55    | 102    |

Notable raw signals (interpret in §7):

- **Frontend modularity diverges sharply**: Claude Code split the client into 7 JS
  modules; Codex shipped a single JS file; Cursor used 2.
- **Test volume diverges ~2.5×**: 139 (code) vs 102 (cursor) vs 55 (codex) test
  functions, despite similar test-file counts.
- **Total code volume is close** (5.1k–6.0k insertions) — size alone does not explain
  the structural differences.

---

## 7. Qualitative Analysis

### 7.1 Architecture & Structure

- **Claude Code** (`rebuild/code`): frontend split into 7 per-view JS modules under
  `frontend/js/` (`app.js` + `quiz-list` / `quiz-builder` / `quiz-preview` / `exam-list` /
  `exam-taking` / `exam-results`), coordinated by a `registerPage` navigation controller;
  15 backend `.py` files with routes, repositories, and validation separated. DB module
  `backend/database.py`.
- **Codex** (`rebuild/codex`): frontend is a single ~1,384-line `frontend/app.js` (one
  `elements` id-cache + one `bindEvents()` + all render functions); 10 backend `.py` files
  (more consolidated). DB module `backend/db.py`.
- **Cursor** (`rebuild/cursor`): 2 frontend JS files (`frontend/js/api.js`,
  `questions.js`); 15 backend `.py`. DB module `backend/db.py`. (From file listing;
  not run this session.)

### 7.2 Data Model & Schema Versioning

The sharpest concrete divergence — same tasks, three different data-layer decisions:

| Aspect                    | Claude Code           | Codex                     | Cursor                    |
| ------------------------- | --------------------- | ------------------------- | ------------------------- |
| Schema versioning         | `PRAGMA user_version` | `schema_migrations` table | `schema_migrations` table |
| `questions` answer column | `correct`             | `correct_answer`          | `correct`                 |
| DB module                 | `backend/database.py` | `backend/db.py`           | `backend/db.py`           |

Observed consequence: the shared dataset (main's `data/quiz_bank.db`, which uses `correct`
and a `schema_migrations` table already at v1–4) drops into Cursor/Claude Code's `correct`
expectation, but **breaks Codex**, whose queries use `correct_answer` — and because
`schema_migrations` already lists 1–3, Codex's own migrations are skipped, so the foreign
schema is reused and every `correct_answer` query fails. Codex is the only tool that
renamed the column, so cross-branch DB reuse needs a translation step for Codex only.
(See `.devflow/memory.md`.)

### 7.3 Test Strategy

- Test functions: Claude Code 139, Cursor 102, Codex 55 (files 18 / 19 / 19). Codex has the
  fewest assertions despite a comparable file count.
- All three suites are Python/pytest only (backend logic + page-module HTML-string checks);
  none drive a real browser DOM. Codex additionally ran `node --check` on its JS — syntax
  only, not DOM behavior.

### 7.4 Correctness & Behavior Parity (this session)

- **Claude Code**: built and verified in-browser this session — Question Bank, Quiz Builder,
  and Online Exam flows rendered and worked.
- **Codex**: shipped a runtime frontend bug — `app.js` referenced two element ids
  (`back-to-exams-button`, `exam-taking-copy`) absent from `index.html`; `bindEvents()`
  threw on the `null` and aborted ALL initialization, so buttons were dead and no `/api/*`
  calls fired. Its evidence marked those flows PASS, but its verification (pytest +
  `node --check`) never exercised the real DOM, so the JS↔HTML contract break slipped
  through. Fixed this session by adding the two elements.
- **Cursor**: not run/debugged this session — parity unverified.

### 7.5 Spec Adherence & Scope

- ACR self-assessment differs: Claude Code and Codex marked every o01–o03 task PASS, while
  Cursor self-reported 2 PARTIAL (both in `o01-e03` — question-bank API endpoints and
  error handling); the rest of Cursor's are PASS. (Per-tool merged tables:
  `*_acr.md` on each branch.)
- Read this as a self-reported **honesty** signal, not a verified completeness gap: Cursor
  was not runtime-verified this session, and Codex's all-PASS ACR still hid a frontend bug
  that broke the shipped UI (see 7.4). An ACR "PASS" does not guarantee the build runs, and
  a "PARTIAL" does not prove a tool did less — verification **depth** varies independently
  of self-reported **coverage**.

### 7.6 Readability & Idiom

- Not systematically compared this session. The clearest structural signal is Codex's
  single monolithic `app.js` versus Claude Code's 7 small modules — a maintainability
  divergence worth a deeper pass.

---

## 8. Summary / Conclusions

- **Volume is similar** across tools (~5.1k–6.0k LOC); the real differences are
  **structural** and in **verification depth**, not size.
- **Two divergences with practical impact**: (a) Codex renamed the answer column to
  `correct_answer` and, like Cursor, uses a `schema_migrations` table — making its DB
  incompatible with the shared seed without translation; (b) Codex's frontend had a
  JS↔HTML mismatch that its non-DOM verification missed.
- **Style spectrum**: Claude Code favored fine-grained modularity (7 JS modules) and the
  most tests; Codex favored consolidation (1 JS file) with the fewest tests; Cursor sits
  between them structurally (2 JS files) — deeper review pending.
- **Method takeaway**: an ACR full of PASS marks is not proof a build runs. Tools that
  verified only backend logic (pytest) and JS syntax (`node --check`) shipped a broken
  UI. A DOM-level smoke check would have caught it.

---

## 9. Method Notes & Caveats

- File counts and LOC are **proxies**, not quality scores — a smaller build is not
  automatically worse, nor a larger one better.
- Metrics were taken from the branch tips; if branches are amended, re-run §5.
- The baseline (`rebuild/base`) intentionally contains no code, so every insertion count
  equals the tool's total contribution.
