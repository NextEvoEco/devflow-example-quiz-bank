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

## 2026-07-07 - Frontend Multi-Page Navigation Controller

- Type: handoff
- Scope: `frontend/` page structure and any new page added in V2/V3
- Detail: The frontend is a single static shell (`frontend/index.html`) with one `<section class="page" id="page-<pageId>">` per view and a shared navigation controller in `frontend/js/app.js`. `navigate(pageId, opts)` hides all `.page` sections, shows `#page-<pageId>`, sets the active sidebar item via `NAV_GROUP` (maps a page to the nav item that should light up, e.g. `quizCreate`→`quizList`), sets the top-bar title via `TOP_BAR_TITLES`, and calls the registered loader. Page modules register a loader with `registerPage(pageId, fn)` (backed by the global `window.pageLoaders`); the loader receives `opts` from `navigate`. Sidebar `.nav-item` buttons use `data-page` and are auto-wired. Valid `currentPage` ids follow `.devflow/context/ui-spec.md`: `questions`, `quizList`, `quizCreate`, `examList`, `examTaking`, `examResults`. To add a page: add a `#page-<id>` section, a nav item (or navigate to it programmatically), and `registerPage("<id>", loader)` from a page-specific JS module. Each page module is its own file (`app.js` = QB + nav, `quiz-list.js` = quizList/quizCreate) to keep modules isolated per conventions.
- Source: implemented in task `o02/t03-quiz-list-page` when converting the single QB page into a multi-page app; t04/t05 (and V3 exam pages) build on this controller.

## 2026-07-07 - Context Files Described Code That Did Not Exist

- Type: caveat
- Scope: repository state verification before executing any task
- Detail: `.devflow/context/architecture.md`, `stack.md`, `dependencies.md`, `repo-structure.md`, and every task file under `.devflow/tasks/` (including `o01/t01`) already described/marked a fully implemented V1-V3 app ("Status: verified", acceptance criteria checked). The actual git history only ever committed DevFlow planning artifacts — `backend/`, `frontend/`, and `tests/` had no tracked source files (only orphaned `__pycache__` bytecode from a prior, uncommitted implementation remained on disk). Do not trust "verified" status or checked acceptance boxes in task files as proof the code exists; always check the real `backend/`, `frontend/`, `tests/` directories (and `git ls-tree`) before assuming a task is already done.
- Source: discovered while executing task `o01/t01-bootstrap-local-web-app` on branch `rebuild/code` — `Glob`/`git ls-tree` showed no `.py` source files despite context files claiming otherwise.
