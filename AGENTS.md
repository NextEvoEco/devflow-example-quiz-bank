# AGENTS.md

This file defines the default operating rules for any AI agent using DevFlow in this repository.

It should stay mostly project-agnostic.
Project-specific details should be written in `.devflow/context/`, `.devflow/memory.md`, and workflow artifacts instead of being hardcoded here.

---

## Project Description

Fill this section when a real project starts.
Leave it blank in the starter repository.

**Project Name:** Quiz Bank (DevFlow example project)

**Project Type:** Local web application

**Project Description:** A lightweight Quiz Bank application used to demonstrate the DevFlow workflow. V1 focuses on Question Bank CRUD with a Python backend, plain HTML/CSS/JavaScript frontend, and SQLite persistence.

**Target Users:** Educators and learners using a local demo application

---

## Purpose

Use DevFlow to keep AI-assisted development resumable, traceable, and structured through Markdown artifacts.

DevFlow separates:

- project bootstrap rules
- project context
- current runtime state
- durable execution memory
- intent, planning, execution, and evidence

---

## DevFlow Usage

### 1. Start With Bootstrap Files

When an AI agent begins work, read files in this order:

```text
1. README.md
2. AGENTS.md
3. CLAUDE.md                    # optional, model-specific
4. .devflow/status.md
5. .devflow/memory.md
6. Current Intent
7. Current Objective
8. Current Task
9. Project Context              # as required
10. Related Evidence            # as required
```

Do not rely on prior chat history when repository artifacts are available.

### 2. Use The Artifact Flow

Every development iteration should follow this flow:

```text
Intent -> Interview -> Objective -> Task -> Execution -> Evidence -> Status
```

Use each artifact for one responsibility only.

### 3. Fill Context Before Complex Execution

Before major implementation begins, fill or update project context as needed:

- `.devflow/context/architecture.md`
- `.devflow/context/stack.md`
- `.devflow/context/dependencies.md`
- `.devflow/context/conventions.md`
- `.devflow/context/repo-structure.md`

If a context file is still empty, do not invent hidden assumptions.
Write the missing context into the proper file when it becomes known.

### 4. Use Templates And Stable Naming

When creating new workflow files:

- use templates from `.devflow/templates/` when available
- follow the naming rules in `README.md`
- keep filenames stable, lowercase, and machine-readable

Recommended conventions:

- intent: `iNN-<slug>.md`
- objective: `oNN-<slug>.md`
- task: `tNN-<slug>.md`
- evidence: `oNN-eNN-<slug>.md`

### 5. Update Runtime State During Work

Use `.devflow/status.md` to track:

- current intent
- current objective
- current task
- current role
- progress
- resume point

Update `.devflow/memory.md` when you discover non-obvious facts that should survive across sessions.

### 6. Keep Scope Explicit

When implementing:

- execute one task at a time
- stay within the current task boundary
- record what was actually done in evidence
- do not silently expand scope across unrelated areas

---

## Repository Structure

### Documentation Records

```text
.devflow/intent/
.devflow/interview/
.devflow/objective/
.devflow/tasks/
.devflow/evidence/
```

### Support And Configuration

```text
.devflow/roles/
.devflow/skills/
.devflow/templates/
.devflow/context/
```

### Execution Control

```text
.devflow/memory.md
.devflow/status.md
AGENTS.md
CLAUDE.md
```

---

## Roles

Role files are stored in `.devflow/roles/`.
Load the role file that matches the current assignment before acting.

Current built-in roles:

- developer
- qa
- task planner
- pm
- interviewer

If role behavior conflicts with this file, use:

1. current task file
2. current role file
3. AGENTS.md
4. README.md

---

## Skills

Skill files are stored in `.devflow/skills/`.
Load the relevant skill before performing a structured workflow action.

Use skills when available for repeatable operations such as:

- interview
- task splitting
- task execution

---

## Writing Rules

Default rules for project files:

- write clearly and explicitly
- keep artifacts structured and scannable
- avoid hidden assumptions
- avoid mixing planning, execution, and evidence in one file
- prefer ASCII filenames and stable identifiers

If the project later defines stricter writing rules, place them in:

- `.devflow/context/conventions.md`
- project-specific objectives or tasks

---

## What Not To Store Here

Do not use `AGENTS.md` for:

- project-specific architecture details
- current task status
- evidence logs
- product-specific business rules
- temporary debugging notes

Store those in the proper DevFlow artifacts instead.

---

## Success Condition

DevFlow is being used correctly when:

- AI can resume work from repository files instead of chat memory
- project-specific knowledge is stored in context, memory, and workflow artifacts
- execution stays aligned with explicit tasks
- evidence records what actually happened
