# Development Status

This file tracks the current runtime state of the repository.

Update it whenever the active intent, objective, task, role, or resume point changes.
Keep it lightweight and current.

---

## Current State

| Field             | Value                                                          |
| ----------------- | -------------------------------------------------------------- |
| Current Intent    | `.devflow/intent/i03-online-exam.md`                           |
| Current Objective | `.devflow/objective/o03-online-exam-v1.md`                     |
| Current Task      | `.devflow/tasks/o03/t06-add-tests-and-release-verification.md` |
| Current Role      | developer                                                      |
| Progress          | completed / verified                                           |
| Resume Point      | Objective O03 complete — full Quiz Bank V1–V3 baseline ready   |
| Next Action       | Review release artifacts or start a new intent for future work |

---

## Active References

| Artifact         | Path                                                              |
| ---------------- | ----------------------------------------------------------------- |
| Intent           | `.devflow/intent/i03-online-exam.md`                              |
| Objective        | `.devflow/objective/o03-online-exam-v1.md`                        |
| Task             | `.devflow/tasks/o03/t06-add-tests-and-release-verification.md`    |
| Related Evidence | `.devflow/evidence/o03-e06-add-tests-and-release-verification.md` |

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
