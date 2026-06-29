# Development Status

This file tracks the current runtime state of the repository.

Update it whenever the active intent, objective, task, role, or resume point changes.
Keep it lightweight and current.

---

## Current State

| Field             | Value |
| ----------------- | ----- |
| Current Intent    |       |
| Current Objective |       |
| Current Task      |       |
| Current Role      |       |
| Progress          |       |
| Resume Point      |       |
| Next Action       |       |

---

## Active References

Fill paths only when the corresponding artifact exists.

| Artifact         | Path |
| ---------------- | ---- |
| Intent           |      |
| Objective        |      |
| Task             |      |
| Related Evidence |      |

---

## Resume Order

Any AI tool resuming work should read files in this order:

```text
1. README.md
2. AGENTS.md
3. CLAUDE.md                    # optional
4. .devflow/status.md           # you are here
5. .devflow/memory.md
6. Current Intent
7. Current Objective
8. Current Task
9. Project Context              # as required
10. Related Evidence            # as required
```

If a referenced artifact does not exist yet, continue with the next relevant file and update the repository state when appropriate.

---

## Update Rules

- Use this file for current runtime state, not durable memory
- Keep entries concise and current
- Replace outdated values instead of appending chat-like logs
- Store cross-session discoveries in `.devflow/memory.md`
- Store completed implementation results in evidence artifacts

---

## Starter Notes

- Leave fields blank until the project starts
- Do not pre-fill old project history into this file
- Keep the structure stable so future AI sessions can resume reliably
