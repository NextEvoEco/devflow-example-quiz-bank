# Skill: Task Split

**Trigger:** user asks to split work into tasks or a confirmed objective is ready for decomposition
**Primary Role:** Task Planner

---

## Purpose

Decompose one confirmed objective into task-sized execution units.

---

## Reading Order

```text
1. README.md
2. AGENTS.md
3. CLAUDE.md                    # optional
4. .devflow/status.md
5. .devflow/memory.md
6. Current Objective
7. Project Context              # as required
```

---

## Steps

### 1. Read The Objective

Confirm:

- scope
- constraints
- deliverables
- success criteria

### 2. Identify Work Units

Break the objective into logical pieces that:

- can be executed independently
- have explicit boundaries
- can be verified without later tasks

### 3. Order By Dependency

- foundation work first
- integration work later
- no circular dependencies

### 4. Write Task Files

For each task:

- use `.devflow/templates/task-template.md`
- save under `.devflow/tasks/o{N}/t{NN}-{slug}.md`
- make acceptance criteria explicit

### 5. Update State

- update `status.md` so the current planning state is visible

---

## Outputs

| Artifact                              | Purpose                     |
| ------------------------------------- | --------------------------- |
| `.devflow/tasks/o{N}/t{NN}-{slug}.md` | executable task definitions |
| `.devflow/status.md`                  | planning state update       |
