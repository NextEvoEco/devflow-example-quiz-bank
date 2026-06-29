# Evidence: {Title}

**ID:** o{N}-e{NN}-{slug}
**Task Ref:** `.devflow/tasks/o{N}/t{NN}-{slug}.md`
**Executed By:** {AI tool name, e.g., Claude Code / Cursor / ChatGPT}
**Execution Date:** YYYY-MM-DD
**Execution Time:** {e.g., 14:30-15:10 UTC+8, ~40 min}
**Status:** completed | partial | blocked

---

## 1. Summary

> One paragraph: what was built, what was verified, what is the state of the deliverables.

{Summary}

---

## 2. Files Changed

| File     | Change Type                  | Description    |
| -------- | ---------------------------- | -------------- |
| `{path}` | created / modified / deleted | {what changed} |
| `{path}` | created / modified / deleted | {what changed} |

---

## 3. Behavior Added

> What the system can now do that it could not do before.

* {Behavior 1}
* {Behavior 2}

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                  | Result             | Notes    |
| -------------------------- | ------------------ | -------- |
| {Criterion from task file} | PASS / FAIL / SKIP | {detail} |
| {Criterion from task file} | PASS / FAIL / SKIP | {detail} |

### Test Output

```
{Paste test run output, CLI output, or screenshot description}
```

---

## 5. Known Limitations

> Anything that was not fully completed, edge cases not handled, or known issues introduced.

* {Limitation 1}
* {Limitation 2 - or "None" if complete}

---

## 6. Next Suggested Task

> What should be executed next, and any context the next session should be aware of.

**Next task:** `{task ID and title}`
**Context:** {Any state the next executor should know that is not obvious from the code}
