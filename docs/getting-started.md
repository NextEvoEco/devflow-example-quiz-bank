# DevFlow Getting Started

## Purpose

This guide explains how to start using DevFlow after downloading the repository.

Use this file when you want the practical setup sequence, not just the conceptual overview.

---

## 1. Download The Repository

Clone the repository:

```bash
git clone <repository-url>
cd devflow
```

Or download the repository as a ZIP and extract it locally.

---

## 2. Understand What Is Already Included

The starter repository already provides:

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.devflow/status.md`
- `.devflow/memory.md`
- `.devflow/context/*.md`
- `.devflow/templates/*.md`
- `.devflow/roles/*.md`
- `.devflow/skills/*.md`

These files are designed to help humans and AI continue work from repository state instead of chat history.

---

## 3. Read The Bootstrap Files First

Before starting a real project, read these files in order:

1. `README.md`
2. `AGENTS.md`
3. `CLAUDE.md` (optional)
4. `.devflow/status.md`
5. `.devflow/memory.md`

This gives you:

- the DevFlow workflow
- the startup rules
- the current runtime state
- any durable execution memory

---

## 4. Fill The Project Description Placeholders

When you begin a real project, fill the project description section in:

- `AGENTS.md`
- `CLAUDE.md`

At minimum, fill:

- project name
- project type
- project description
- target users

Do not put detailed architecture or task-level information into these two files.
Keep project-specific detail in the DevFlow artifacts below.

---

## 5. Fill The Project Context Files

Next, fill the context files that define the project background:

- `.devflow/context/architecture.md`
- `.devflow/context/stack.md`
- `.devflow/context/dependencies.md`
- `.devflow/context/conventions.md`
- `.devflow/context/repo-structure.md`

You do not need to fill everything immediately.
Only add confirmed information.

Recommended order:

1. `stack.md`
2. `repo-structure.md`
3. `conventions.md`
4. `architecture.md`
5. `dependencies.md`

---

## 6. Start The First DevFlow Iteration

A normal first iteration usually follows this order:

1. Create an intent artifact
2. Conduct interview and clarify the request
3. Write a confirmed objective
4. Split the objective into tasks
5. Execute one task
6. Write evidence
7. Update status

Use the templates in `.devflow/templates/` whenever a matching template exists.

Typical files created during the first iteration:

```text
.devflow/intent/i01-<slug>.md
.devflow/interview/i01-<slug>.md
.devflow/objective/o01-<slug>.md
.devflow/tasks/o01/t01-<slug>.md
.devflow/evidence/o01-e01-<slug>.md
```

---

## 7. How To Use The Templates

Use these templates as the default starting point:

- `.devflow/templates/intent-template.md`
- `.devflow/templates/interview-template.md`
- `.devflow/templates/objective-template.md`
- `.devflow/templates/task-template.md`
- `.devflow/templates/evidence-template.md`
- `.devflow/templates/status-template.md`
- `.devflow/templates/memory-template.md`

These templates are intentionally structured so AI can fill them predictably.

---

## 8. What To Keep Empty

These files may remain empty until a real project begins:

- `.devflow/intent/.gitkeep`
- `.devflow/interview/.gitkeep`
- `.devflow/objective/.gitkeep`
- `.devflow/tasks/.gitkeep`
- `.devflow/evidence/.gitkeep`

These are directory placeholders only.

Do not leave these as raw empty files:

- `AGENTS.md`
- `CLAUDE.md`
- `.devflow/status.md`
- `.devflow/memory.md`
- `.devflow/context/*.md`
- `.devflow/templates/*.md`

They should always contain guidance or structure.

---

## 9. Where Different Types Of Information Belong

Use this split consistently:

### Bootstrap Rules

Put general operating rules in:

- `AGENTS.md`
- `CLAUDE.md`

### Project Context

Put project background in:

- `.devflow/context/*.md`

### Runtime State

Put current progress and resume state in:

- `.devflow/status.md`

### Durable Memory

Put non-obvious cross-session knowledge in:

- `.devflow/memory.md`

### Workflow Artifacts

Put actual iteration work in:

- `.devflow/intent/`
- `.devflow/interview/`
- `.devflow/objective/`
- `.devflow/tasks/`
- `.devflow/evidence/`

---

## 10. Minimal First-Use Checklist

Use this checklist after download:

- Read `README.md`
- Read `AGENTS.md`
- Read `CLAUDE.md` if relevant
- Fill project description placeholders
- Fill at least `stack.md`, `repo-structure.md`, and `conventions.md`
- Create the first intent file
- Run the first interview
- Confirm the first objective
- Split the objective into tasks
- Execute one task only

---

## 11. Run The Quiz Bank Application

After the V1 foundation task is complete, use:

- [docs/app-startup.md](docs/app-startup.md) for installation and startup
- [docs/v1-verification.md](docs/v1-verification.md) for the V1 release checklist
- [docs/o02-verification.md](docs/o02-verification.md) for the Quiz Builder V1 release checklist

---

## 12. Success Condition

You are using DevFlow correctly when:

- another AI session can continue from repository files alone
- project-specific knowledge is written into the proper artifacts
- tasks stay bounded
- evidence reflects what actually happened
- status reflects where work should resume
