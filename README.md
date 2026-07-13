# DevFlow Example — Quiz Bank

> A reference implementation demonstrating how DevFlow structures AI-assisted software development through a real project.

This repository is the official reference implementation of **DevFlow**.

Rather than explaining the workflow through abstract concepts, this project demonstrates how DevFlow artifacts evolve while building a complete Quiz Bank application—from the initial idea to a working product.

Every development decision is preserved as part of the project itself, allowing both humans and AI to continue development across sessions without relying on conversation history.

---

# Purpose

This repository demonstrates how DevFlow organizes software development into persistent project artifacts.

Instead of treating AI conversations as project memory, DevFlow stores project state directly inside the repository.

By following this example, you can see:

* How a project starts from an initial intent.
* How requirements are clarified through interviews.
* How objectives become executable tasks.
* How execution progress is tracked.
* How project context remains independent from conversations.
* How development decisions are preserved as evidence.

---

# What This Repository Demonstrates

This project builds a simple Quiz Bank application.

The application itself is intentionally small.

The primary purpose is to demonstrate the DevFlow workflow rather than application complexity.

Current development roadmap:

* V1 — Question Bank
* V2 — Quiz Builder
* V3 — Online Exam

Each version introduces additional DevFlow artifacts while keeping the application understandable.

---

# Repository Structure

```text
.devflow/
    intent/         Project intent for each iteration
    interview/      Requirement clarification records
    objective/      Version objectives
    tasks/          Individual executable tasks
    evidence/       Development evidence and decision records
    context/        Project environment
                        - architecture
                        - technology stack
                        - conventions
                        - dependencies
    status.md       Execution progress
    memory.md       Durable cross-session knowledge
    roles/          AI role definitions
    skills/         AI skill definitions
    templates/      Artifact templates

docs/
    Supporting documentation

src/
    Application source code
```

---

# Development Philosophy

DevFlow separates **project state** from **AI conversations**.

Instead of depending on a chat history, every important decision is externalized into structured Markdown artifacts.

This allows development to continue across:

* new AI sessions
* different AI models
* different engineers
* different development tools

without reconstructing project context from scratch.

---

# Learning Path

The recommended reading order is:

1. `.devflow/status.md` — current execution state
2. `.devflow/intent/` — project intent artifacts
3. `.devflow/interview/` — requirement clarification records
4. `.devflow/objective/` — confirmed objectives
5. `.devflow/tasks/` — individual executable tasks
6. `.devflow/evidence/` — development decisions and outcomes
7. `.devflow/context/` — project environment reference

Following this order shows how an idea gradually becomes executable software.

If you are new to DevFlow and want to apply it to your own project, see [docs/getting-started.md](docs/getting-started.md).

---

# Experiments & Demonstrations

## Refactor Stack Experiment

This repository contains a **multi-stack refactor experiment** that demonstrates DevFlow's core principle: **a single artifact set can drive multiple implementation stacks**.

### How It Works

1. **Shared Specification** (`refactor/base`): All stacks start from identical DevFlow artifacts
   - Intent documents
   - Interview clarifications
   - Objectives
   - Task definitions
   - Context files (architecture, conventions, dependencies)

2. **Stack Implementations**: Each stack rebuilds the same application independently
   - `refactor/python-vue-sqlite`: Python/Flask backend, Vue 3 frontend, SQLite database
   - `refactor/java-react-postgre`: Java/Spring Boot backend, React frontend, PostgreSQL database

3. **Cross-Stack Analysis** (`refactor/compare`):
   - [docs/refactor-index.md](docs/refactor-index.md) — reading guide and quick reference
   - [docs/refactor-comparison.md](docs/refactor-comparison.md) — full quantitative and qualitative analysis

### Key Findings

- **Both stacks completed 100% of the specification** (87 acceptance criteria, 3 full versions)
- **Code volume is comparable** (~6.5k–8.1k LOC) despite language/framework differences
- **Architecture diverges by idiom** (lightweight/convention vs. explicit/layered)
- **Database choice has real trade-offs** (zero-setup SQLite vs. production-grade PostgreSQL)

See [docs/refactor-index.md](docs/refactor-index.md) to start exploring.

---

# Relationship to DevFlow

This repository is a reference implementation.

The DevFlow framework itself is maintained separately.

**DevFlow Framework**

https://github.com/NextEvoEco/devflow

This repository focuses on demonstrating how DevFlow is applied in practice through:

- **Progressive development**: Show how intent → interview → objectives → tasks → evidence flows
- **Multi-stack validation**: Prove the same spec works across different technology stacks
- **Cross-session resilience**: All project state lives in the repository, not in conversations

---

# Status & Branches

## Main Development Branch

This repository uses a multi-branch strategy to demonstrate DevFlow across different technology stacks.

### Active Branches

| Branch | Stack | Status | Purpose |
|--------|-------|--------|---------|
| `refactor/base` | — | ✅ Complete | Shared baseline (DevFlow artifacts only) |
| `refactor/python-vue-sqlite` | Python + Flask / Vue 3 + TypeScript / SQLite | ✅ Complete | First stack implementation |
| `refactor/java-react-postgre` | Java 21 + Spring Boot 3 / React 18 + TypeScript / PostgreSQL + Flyway | ✅ Complete | Second stack implementation |
| `refactor/compare` | — | ✅ Complete | Cross-stack analysis hub |

### Completed Versions (All Stacks)

* **V1 — Question Bank** ✅ (all stacks)
* **V2 — Quiz Builder** ✅ (all stacks)
* **V3 — Online Exam** ✅ (all stacks)

All versions fully implemented and verified across both technology stacks.

### Refactor Experiment

The repository demonstrates a **multi-stack refactor experiment** where the same DevFlow specification drives implementations in different technology stacks:

- **Python/Vue/SQLite**: Lightweight, convention-over-configuration approach
- **Java/React/PostgreSQL**: Production-grade, explicit-architecture approach

See [docs/refactor-index.md](docs/refactor-index.md) for a reading guide and quick links.

---

# License

MIT License
