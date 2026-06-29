# Skill: Execute Task

**Trigger:** user asks to execute a task, continue current work, or resume from status
**Primary Roles:** Developer, QA

---

## Purpose

Execute one task, verify it, and leave the repository in a resumable state.

---

## Reading Order

Before starting:

```text
1. README.md
2. AGENTS.md
3. CLAUDE.md                    # optional
4. .devflow/status.md
5. .devflow/memory.md
6. Current Intent
7. Current Objective
8. Current Task
9. Project Context              # as required
10. Related Evidence            # as required
```

---

## Steps

### 1. Identify The Task

- use the current task from `status.md`, or
- use the task explicitly requested by the user

### 2. Read The Task Fully

Confirm:

- purpose
- scope
- constraints
- inputs
- outputs
- acceptance criteria

### 3. Implement

- stay within the task boundary
- update `status.md` as work progresses
- record durable discoveries in `memory.md` if needed

### 4. Verify

- check the acceptance criteria
- record evidence in an evidence artifact
- mark the task verified or blocked based on actual results

### 5. Leave A Resumable State

Before stopping:

- ensure `status.md` reflects the latest runtime state
- ensure evidence exists if verification happened
- ensure durable discoveries are stored in `memory.md`

---

## Outputs

| Artifact                                 | Purpose                               |
| ---------------------------------------- | ------------------------------------- |
| source changes                           | implementation                        |
| `.devflow/status.md`                     | runtime state                         |
| `.devflow/memory.md`                     | durable non-obvious facts when needed |
| `.devflow/evidence/o{N}-e{NN}-{slug}.md` | verification record                   |
