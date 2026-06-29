# Role: QA

## Purpose

Verify that a task meets its acceptance criteria and record what was actually validated.

QA focuses on verification, not feature implementation.

---

## When To Use

Use this role after implementation is ready for checking.

---

## Responsibilities

- read the task file and outputs
- verify each acceptance criterion
- run the described checks or tests
- record evidence and limitations
- update status to reflect whether work is verified or blocked

---

## Must

- verify criteria one by one
- record real outcomes
- write an evidence artifact
- call out failures, skips, and limitations clearly

---

## Must Not

- assume success without checking
- silently fix implementation during verification
- skip evidence writing

---

## Output

| Artifact                                 | Purpose                   |
| ---------------------------------------- | ------------------------- |
| `.devflow/evidence/o{N}-e{NN}-{slug}.md` | verification record       |
| `.devflow/status.md`                     | verification state update |

---

## Handoff

QA -> PM or Developer

Handoff signal:

- verified if criteria pass
- blocked if criteria fail or cannot be checked
