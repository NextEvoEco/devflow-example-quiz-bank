# Task: Build Question Storage And Validation

**ID:** o01/t02-build-question-storage-and-validation
**File:** `.devflow/tasks/o01/t02-build-question-storage-and-validation.md`
**Objective Ref:** `.devflow/objective/o01-question-bank-v1.md`
**Depends On:** o01/t01-bootstrap-local-web-app
**Complexity:** M
**Estimated Duration:** 1 hr
**Status:** verified

---

## 1. Purpose

> What does this task accomplish within the objective?

This task creates the Question Bank data model, SQLite persistence layer, and validation rules so API and UI work can rely on a single source of truth for question behavior.

---

## 2. Boundary

### In Scope

* Define the Question entity and SQLite schema for V1.
* Implement create, read, update, delete, and search persistence operations for questions.
* Implement validation rules for question text, options A-D, correct answer, and difficulty defaults.
* Define error behavior for invalid question payloads at the domain or service layer.

### Out of Scope

* HTTP routing.
* Frontend rendering and interaction logic.
* Quiz-related data structures.

---

## 3. Must / Must Not

### Must

* Enforce required fields for question text, options A-D, and correct answer.
* Apply a default difficulty value when one is not explicitly provided.
* Keep the storage and validation layer reusable by later API and test tasks.

### Must Not

* Embed validation only in the frontend.
* Introduce schema for out-of-scope quiz or exam features.

---

## 4. Inputs

| Artifact | Source |
| --- | --- |
| Objective definition | `.devflow/objective/o01-question-bank-v1.md` |
| Bootstrap app structure | `o01/t01-bootstrap-local-web-app` |
| Question data model guidance | `.devflow/context/ui-spec.md` |

---

## 5. Outputs

| Artifact | Path |
| --- | --- |
| Question model, storage, and validation code | `backend/` |
| SQLite schema or migration bootstrap updates | `backend/` |
| Automated tests for validation/storage behavior | `tests/` |

---

## 6. Acceptance Criteria

> These criteria must all pass before the task is marked complete.

* [x] Questions can be inserted, updated, deleted, listed, and searched through the persistence layer.
* [x] Invalid question data is rejected according to the V1 validation rules.
* [x] Difficulty receives a default value when omitted.

---

## 7. Test Plan

```text
1. Run automated tests for the question storage and validation layer.
2. Verify CRUD and search operations against SQLite.
3. Verify invalid payloads fail with explicit validation errors.
4. Verify omitted difficulty is replaced with the default value.
```

---

## 8. Notes

This task should define reusable backend behavior without assuming any specific frontend flow.
