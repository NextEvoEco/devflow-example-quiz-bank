# CLAUDE.md

This file provides Claude-specific guidance for using DevFlow in this repository.

It should remain mostly project-agnostic.
Project-specific information should be written in `.devflow/context/`, `.devflow/memory.md`, and workflow artifacts.

---

## Project Description

Fill this section when a real project starts.
Leave it blank in the starter repository.

**Project Name:** {fill when project starts}

**Project Type:** {fill when project starts}

**Project Description:** {fill when project starts}

**Target Users:** {fill when project starts}

---

## Claude Role In DevFlow

When Claude works inside a DevFlow repository, it should:

- reconstruct state from repository artifacts first
- ask clarifying questions during interview when uncertainty matters
- use explicit artifact boundaries
- avoid relying on hidden conversational memory
- write back durable knowledge into DevFlow files

Claude should behave like a structured collaborator, not like a free-form chat log.

---

## Claude Reading Order

Before implementation or planning, read in this order:

```text
1. README.md
2. AGENTS.md
3. CLAUDE.md
4. .devflow/status.md
5. .devflow/memory.md
6. Current Intent
7. Current Objective
8. Current Task
9. Project Context              # as required
10. Related Evidence            # as required
```

If a file is missing, continue with the next relevant artifact and record the gap when needed.

---

## How Claude Should Use DevFlow

### 1. During Initialization

When the repository is still a starter:

- keep project description placeholders empty until the user provides real project details
- do not invent project architecture, tech stack, or business goals
- fill context files only when information is confirmed

### 2. During Interview

When intent is incomplete:

- capture the user need as intent
- ask targeted clarifying questions
- reduce ambiguity before creating or confirming an objective

### 3. During Planning

When an objective is clear:

- define scope, constraints, deliverables, and success criteria
- split work into task-sized units
- make task boundaries explicit enough for a fresh AI session

### 4. During Execution

When a current task exists:

- implement only the current task
- keep changes aligned with the task boundary
- update status as work progresses
- record non-obvious discoveries in memory
- produce evidence after execution or verification

### 5. During Resume

When resuming after interruption:

- trust repository state over chat memory
- use `status.md` to find the current position
- use `memory.md` to recover non-obvious facts
- use context files to reconstruct project understanding

---

## Claude Output Principles

Claude should prefer output that is:

- structured
- explicit
- resumable
- traceable
- easy for another model to continue

Claude should avoid:

- hidden assumptions
- mixing unrelated tasks
- burying important state only in chat replies
- inventing project constraints that are not documented

---

## Working With Templates

When creating new artifacts:

- use `.devflow/templates/` when a matching template exists
- preserve headings and placeholder structure unless there is a good reason to adjust them
- keep the file easy for both humans and models to scan

If a needed template does not exist:

- follow the structure defined in `README.md`
- create the artifact with stable headings and explicit fields

---

## Working With Context

Use `.devflow/context/` for project-specific knowledge such as:

- architecture
- tech stack
- dependencies
- conventions
- repository structure

Claude should not hardcode that information into `CLAUDE.md`.

---

## Working With Status And Memory

Use `.devflow/status.md` for current runtime state:

- what is active now
- what is next
- where work should resume

Use `.devflow/memory.md` for durable, cross-session knowledge:

- non-obvious facts
- confirmed constraints
- recurring caveats
- useful handoff notes

Do not use either file as a substitute for task, objective, or evidence artifacts.

---

## What Claude Should Not Do

Claude should not:

- treat old project-specific text as current truth without verification
- write implementation evidence into planning files
- change task scope without making that change explicit
- skip artifact updates when the repository depends on them for resumption

---

## Success Condition

Claude is using DevFlow correctly when another AI session can continue the work by reading repository files, without needing the original conversation.
