# Task: {Title}

**ID:** o{N}/t{NN}-{slug}
**File:** `.devflow/tasks/o{N}/t{NN}-{slug}.md`
**Objective Ref:** `.devflow/objective/o{N}-{slug}.md`
**Depends On:** {task ID or "none"}
**Complexity:** S | M | L
**Estimated Duration:** {e.g., 30 min, 1 hr}
**Status:** pending | in_progress | completed | blocked

---

## 1. Purpose

> What does this task accomplish within the objective?

{One paragraph. Describe what will exist after this task completes that did not exist before.}

---

## 2. Boundary

### In Scope

* {What this task must implement}
* {What this task must implement}

### Out of Scope

* {What this task must NOT implement, even if tempting}
* {Features that belong to other tasks}

---

## 3. Must / Must Not

### Must

* {Hard requirement 1}
* {Hard requirement 2}

### Must Not

* {Hard prohibition 1 - safety, scope, or quality constraint}
* {Hard prohibition 2}

---

## 4. Inputs

| Artifact                                 | Source            |
| ---------------------------------------- | ----------------- |
| {Config file / prior task output / data} | {path or task ID} |

---

## 5. Outputs

| Artifact                | Path   |
| ----------------------- | ------ |
| {Source file or report} | {path} |
| {Test file}             | {path} |

---

## 6. Acceptance Criteria

> These criteria must all pass before the task is marked complete.

* [ ] {Specific, testable criterion - not vague}
* [ ] {Specific, testable criterion}
* [ ] {Specific, testable criterion}

---

## 7. Test Plan

> How to verify the acceptance criteria.

```
{Command to run, or manual steps to verify}
```

---

## 8. Notes

> Implementation hints, known risks, or links to relevant docs.

{Optional. Leave blank if none.}
