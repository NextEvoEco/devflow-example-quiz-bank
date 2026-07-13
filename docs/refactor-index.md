# Refactor Stack Comparison — Reading Guide

Start here. This page orients you to the refactor experiment and points to the detailed
analysis and evidence. For depth, follow the links — this guide does not repeat them.

---

## What this is

Several branches reconstruct the **same** Quiz Bank application from the **same** DevFlow
artifacts (intent, interview, objective, tasks), each using a different **technology stack**.
The question: *given one identical specification, how differently do different stacks build
it?* This branch (`refactor/compare`) is the neutral hub that collects and analyzes the results.

---

## Where things live

| Artifact                                                     | What it is                                                                              |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| [refactor-comparison.md](refactor-comparison.md)             | The full cross-stack analysis — methodology, metrics, qualitative findings, conclusions |
| [python_acr.md](python_acr.md) · [java_acr.md](java_acr.md)  | Per-stack merged **Acceptance Criteria** tables (one row per criterion, all objectives) |
| `screenshots/<stack>_*.png`                                  | Browser verification captures, on each `refactor/<stack>` branch                        |
| `refactor/base` (`43b8f8d`)                                  | Shared baseline — DevFlow artifacts only, **no application code**                       |
| `refactor/python-vue-sqlite` · `refactor/java-react-postgre` | Each stack's implementation (one commit on top of the baseline)                         |

---

## The stacks

| Branch                        | Backend                 | Frontend              | Database            | Status      |
| ----------------------------- | ----------------------- | --------------------- | ------------------- | ----------- |
| `refactor/python-vue-sqlite`  | Python + Flask          | Vue 3 + TypeScript    | SQLite              | ✅ Complete |
| `refactor/java-react-postgre` | Java 21 + Spring Boot 3 | React 18 + TypeScript | PostgreSQL + Flyway | ✅ Complete |

---

## How to explore

```bash
# What one stack built on top of the shared baseline
git diff refactor/base refactor/python-vue-sqlite -- backend frontend tests
git diff refactor/base refactor/java-react-postgre -- backend frontend tests

# Two stacks head-to-head
git diff refactor/python-vue-sqlite refactor/java-react-postgre -- backend frontend tests

# View the comparison
git show refactor/compare:docs/refactor-comparison.md
```

- Compare the two `*_acr.md` side by side to see where task completion and criteria
  alignment differ.
- Full measurement recipe: see **§5 Comparison Methodology** in
  [refactor-comparison.md](refactor-comparison.md).

---

## Results at a glance

| Metric                  | Python/Vue    | Java/React    |
| ----------------------- | ------------- | ------------- |
| **Backend files**       | 13 `.py`      | 26 `.java`    |
| **Frontend files**      | 27 files      | 32 files      |
| **Test files**          | 8 (pytest)    | 19 (JUnit 5)  |
| **Code volume**         | 8,135 LOC     | 6,481 LOC     |
| **Setup time**          | ~5 min        | ~15 min       |
| **Acceptance Criteria** | ✅ 87/87 PASS | ✅ 87/87 PASS |

### Key findings

- **Both stacks completed the spec exactly.** No scope creep in either direction.
- **Architecture diverges by framework idiom**: Flask/Vue are lightweight and
  convention-driven; Spring Boot/React are explicit and layered.
- **Database choice has real consequences**: SQLite is zero-setup; PostgreSQL requires
  a service but is production-grade and enables real-world DB concepts.
- **Test granularity varies by stack**: Python/Vue had 8 test files; Java/React has 19
  (more per-layer structure). Both verified in-browser with identical acceptance criteria.
- **Frontend modularity is comparable**: 27 Vue files vs. 32 React files — both stacks
  favored component-based organization despite different frameworks.

→ Full reasoning, metrics, and architecture analysis: **§6–§8** of
[refactor-comparison.md](refactor-comparison.md).

---

## Stack trade-offs

### Python + Flask + Vue + SQLite

**Strengths:**
- **Simplest bootstrap** — no database service needed, single `py -m backend` command
- **Lightweight framework** — Flask is minimal, fewer abstractions to learn
- **Familiar patterns** — SQLite and Flask are widely taught in CS courses
- **File-based DB** — easy backup, seed data ships in the repo

**Weaknesses:**
- **SQLite doesn't scale** — fine for demo, breaks with concurrent writes or large datasets
- **Fewer explicit boundaries** — convention-over-configuration can hide errors
- **Less relevant to production** — most real systems use PostgreSQL / Spring Boot

### Java + Spring Boot + React + PostgreSQL

**Strengths:**
- **Production-grade stack** — Java, Spring Boot, PostgreSQL are industry standard
- **Explicit architecture** — layered structure makes large codebases maintainable
- **Real database concepts** — foreign keys, indexing, complex queries possible
- **More test granularity** — per-layer testing (repositories, controllers) is clearer

**Weaknesses:**
- **More setup overhead** — JDK + PostgreSQL + Node.js takes ~15 min to install
- **Verbose syntax** — Java has more boilerplate than Python
- **Steeper learning curve** — Spring Boot is more complex than Flask
- **Service dependency** — PostgreSQL must be running; can't commit the DB to git

---

## For future refactor branches

The experiment proves DevFlow's core principle:

1. **A single artifact set can drive multiple stacks** — no modification to intent,
   objectives, or tasks needed (only context files for tech-specific details).
2. **The specification is stack-agnostic** — the behavior contract (API routes, JSON,
   port 5000) ensures interoperability regardless of implementation language.
3. **Schema contracts matter** — preserve **logical** table/column names across branches
   so seed data can move freely (e.g., `questions.correct`, `option_a..d`).
4. **Different stacks make different trade-offs** — there is no "best" stack, only
   trade-offs between simplicity (SQLite) and production-readiness (PostgreSQL).

---

## Related evidence

- **Full Analysis:** [refactor-comparison.md](refactor-comparison.md)
- **Acceptance Criteria (per stack):**
  - Python/Vue: [python_acr.md](python_acr.md)
  - Java/React: [java_acr.md](java_acr.md)
- **Architecture Decisions:**
  - Python/Vue: See `refactor/python-vue-sqlite` branch
  - Java/React: [ADR-01-java-react-postgresql-full-stack.md](ADR-01-java-react-postgresql-full-stack.md)
- **Screenshots:** `screenshots/<stack>_*.png` on each `refactor/<stack>` branch
- **Cross-session caveats / handoff notes:** `.devflow/memory.md` on the stack branches
- **Installation & Setup:** [installation-guide.md](installation-guide.md)

---

## Quick links

| Resource                                       | Purpose                                                      |
| ---------------------------------------------- | ------------------------------------------------------------ |
| `refactor/python-vue-sqlite` commit `dba729a`  | First complete refactor (Python/Flask/Vue/SQLite)            |
| `refactor/java-react-postgre` commit `5a54cd3` | Second complete refactor (Java/Spring Boot/React/PostgreSQL) |
| `refactor/base` commit `43b8f8d`               | Shared baseline — start here if building a new stack         |
| `.devflow/intent/i04-java-react-postgresql.md` | Intent document for the Java stack branch                    |
| `docs/tech-stack.md`                           | General guide for running a refactor experiment              |

---

**Date:** 2026-07-13  
**Stacks compared:** 2 (Python/Vue/SQLite, Java/React/PostgreSQL)  
**All objectives verified:** Yes (V1 Question Bank, V2 Quiz Builder, V3 Online Exam)  
**All acceptance criteria PASS:** Yes (87/87 on both stacks)
