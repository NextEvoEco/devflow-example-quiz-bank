# DevFlow Example - Quiz Bank

> A reference implementation demonstrating how DevFlow structures AI-assisted software development through a real project.

This repository is the official reference implementation of **DevFlow**.

Rather than explaining the workflow through abstract concepts, this project demonstrates how DevFlow artifacts evolve while building a Quiz Bank application from the initial idea to a working product.

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

* V1 - Question Bank
* V2 - Quiz Builder
* V3 - Online Exam

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

backend/
    Flask app, startup entrypoint, and SQLite bootstrap

frontend/
    Static HTML, CSS, and JavaScript assets

tests/
    Automated bootstrap and integration checks

docs/
    Supporting documentation
screenshots/
    Browser verification captures for this rebuild (codex_*.png)
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

# Rebuild Comparison Experiment

This repository is also used as a controlled experiment:
**can different AI coding tools rebuild the same application from the same DevFlow artifacts, and how do the results differ?**

Every implementation branch shares one starting point — the DevFlow artifacts
(intent, interview, objective, tasks) frozen at branch `rebuild/base`, which contains
**no application code**. From that identical specification, each branch reconstructs the
Quiz Bank application using a different AI tool:

| Branch           | AI Tool     | Contents                                 |
| ---------------- | ----------- | ---------------------------------------- |
| `rebuild/base`   | —           | DevFlow artifacts only (shared baseline) |
| `rebuild/code`   | Claude Code | Implementation built by Claude Code      |
| `rebuild/codex`  | Codex       | Implementation built by Codex            |
| `rebuild/cursor` | Cursor      | Implementation built by Cursor           |

Because every branch starts from the same tasks, comparing them
(`git diff rebuild/base rebuild/<tool>`, or two tool branches against each other)
isolates how each tool interprets and executes an identical DevFlow specification —
architecture choices, code structure, test coverage, and adherence to task boundaries.

**This branch (`rebuild/codex`) is the Codex rebuild.**

The cross-tool analysis (methodology + metrics) lives in
[docs/rebuild-comparison.md](docs/rebuild-comparison.md).

## Rebuild Artifacts (this branch)

Tool-specific artifacts use a `codex_` prefix so results from different tools never collide:

- `.devflow/evidence/codex_acr.md` — a single merged **Acceptance Criteria** table
  consolidating every `.devflow/evidence/o0*-e0*.md` result into one view.
- `screenshots/codex_*.png` — browser verification captures of the V1/V2/V3 flows.

---

# Learning Path

The recommended reading order is:

1. `.devflow/status.md` - current execution state
2. `.devflow/intent/` - project intent artifacts
3. `.devflow/interview/` - requirement clarification records
4. `.devflow/objective/` - confirmed objectives
5. `.devflow/tasks/` - individual executable tasks
6. `.devflow/evidence/` - development decisions and outcomes
7. `.devflow/context/` - project environment reference

Following this order shows how an idea gradually becomes executable software.

If you are new to DevFlow and want to apply it to your own project, see [docs/getting-started.md](docs/getting-started.md).

---

# Relationship to DevFlow

This repository is a reference implementation.

The DevFlow framework itself is maintained separately.

**DevFlow Framework**

https://github.com/NextEvoEco/devflow

This repository focuses on demonstrating how DevFlow is applied in practice.

---

# Status

* V1 - Question Bank (Complete)
* V2 - Quiz Builder (Complete)
* V3 - Online Exam (Complete)

---

# Local Startup

Install dependencies:

```text
py -m pip install -r requirements.txt
```

Start the local app:

```text
py -m backend
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Run the bootstrap test suite:

```text
py -m pytest
```

For the V1 release demo and manual verification checklist, see [docs/v1-question-bank-release.md](docs/v1-question-bank-release.md).

For the V2 Quiz Builder release walkthrough, see [docs/v2-quiz-builder-release.md](docs/v2-quiz-builder-release.md).

For the V3 Online Exam release walkthrough, see [docs/v3-verification.md](docs/v3-verification.md).

---

# License

MIT License
