# Skill: Interview

**Trigger:** user starts a new request, asks to clarify requirements, or begins a new cycle
**Primary Roles:** Interviewer, PM

---

## Purpose

Clarify intent before planning and produce the inputs needed for objective definition.

---

## Reading Order

```text
1. README.md
2. AGENTS.md
3. CLAUDE.md                    # optional
4. .devflow/status.md
5. .devflow/memory.md
6. Existing intent, objective, or context files as needed
```

---

## Steps

### 1. Capture The Request

- identify the user need
- preserve the original motivation

### 2. Ask Clarifying Questions

Focus on:

- goal
- scope
- constraints
- success criteria
- open questions

### 3. Summarize

- separate confirmed facts from unresolved items
- ask the user to confirm the summary

### 4. Write Artifacts

Create or update:

- an intent artifact
- an interview artifact
- an objective draft when clarification is sufficient

---

## Outputs

| Artifact                             | Purpose                                |
| ------------------------------------ | -------------------------------------- |
| `.devflow/intent/i{NN}-{slug}.md`    | original request record                |
| `.devflow/interview/i{NN}-{slug}.md` | clarified interview record             |
| `.devflow/objective/o{NN}-{slug}.md` | objective draft or confirmed objective |
