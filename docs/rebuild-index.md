# Rebuild Comparison — Reading Guide

Start here. This page orients you to the rebuild experiment and points to the detailed
analysis and evidence. For depth, follow the links — this guide does not repeat them.

---

## What this is

Several branches reconstruct the **same** Quiz Bank application from the **same** DevFlow
artifacts (intent, interview, objective, tasks), each using a different AI coding tool. The
question: *given one identical specification, how differently do the tools build it?* This
branch (`rebuild/compare`) is the neutral hub that collects and analyzes the results.

---

## Where things live

| Artifact                                                                                   | What it is                                                                             |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| [rebuild-comparison.md](rebuild-comparison.md)                                             | The full cross-tool analysis — methodology, metrics, qualitative findings, conclusions |
| [code_acr.md](code_acr.md) · [codex_acr.md](codex_acr.md) · [cursor_acr.md](cursor_acr.md) | Per-tool merged **Acceptance Criteria** tables (one row per criterion, all objectives) |
| `screenshots/<tool>_*.png`                                                                 | Browser verification captures, on each `rebuild/<tool>` branch                         |
| `rebuild/base` (`c105cbd`)                                                                 | Shared baseline — DevFlow artifacts only, **no application code**                      |
| `rebuild/code` · `rebuild/codex` · `rebuild/cursor`                                        | Each tool's implementation (one commit on top of the baseline)                         |

---

## How to explore

```bash
# What one tool built on top of the shared baseline
git diff rebuild/base rebuild/<tool> -- backend frontend tests

# Two tools head-to-head
git diff rebuild/<toolA> rebuild/<toolB> -- backend frontend tests
```

- Compare the three `*_acr.md` side by side to see where self-assessment diverges.
- Full measurement recipe: see **§5 Comparison Methodology** in
  [rebuild-comparison.md](rebuild-comparison.md).

---

## Results at a glance

- **Volume is similar** (~5–6k LOC each) — the real differences are **structural** and in
  **verification depth**, not size.
- **Frontend modularity diverges sharply**: Claude Code 7 JS modules · Codex 1 · Cursor 2.
- **An all-PASS ACR is not proof it runs**: Codex marked every criterion PASS but shipped a
  JS↔HTML bug its non-DOM verification missed.

→ Full reasoning and the metrics table: **§6–§8** of
[rebuild-comparison.md](rebuild-comparison.md).

---

## Related evidence

- **Analysis:** [rebuild-comparison.md](rebuild-comparison.md)
- **Acceptance Criteria (per tool):** [code_acr.md](code_acr.md),
  [codex_acr.md](codex_acr.md), [cursor_acr.md](cursor_acr.md)
- **Screenshots:** `screenshots/<tool>_*.png` on each `rebuild/<tool>` branch
- **Cross-session caveats / handoff notes:** `.devflow/memory.md` on the tool branches
