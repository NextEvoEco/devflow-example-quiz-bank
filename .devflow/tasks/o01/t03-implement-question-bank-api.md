# Task: Implement Question Bank API

**ID:** o01/t03-implement-question-bank-api
**File:** `.devflow/tasks/o01/t03-implement-question-bank-api.md`
**Objective Ref:** `.devflow/objective/o01-question-bank-v1.md`
**Depends On:** o01/t02-build-question-storage-and-validation
**Complexity:** M
**Estimated Duration:** 1 hr
**Status:** verified

---

## 1. Purpose

> What does this task accomplish within the objective?

This task exposes the Question Bank backend through HTTP endpoints so the frontend can list, search, add, edit, and delete questions using the SQLite-backed application layer.

---

## 2. Boundary

### In Scope

* Add HTTP endpoints for list, search, create, update, and delete question flows.
* Map validation and persistence errors to basic V1 error responses.
* Return payloads that are sufficient for the plain JavaScript frontend to render the Question Bank page.

### Out of Scope

* Final frontend UI behavior.
* Quiz Builder or Online Exam endpoints.
* Authentication, authorization, or multi-user concerns.

---

## 3. Must / Must Not

### Must

* Support Question Bank list and search behavior required by V1.
* Return meaningful error responses for invalid requests and missing records.
* Keep the API lightweight and local-app appropriate.

### Must Not

* Add endpoints for out-of-scope features.
* Hide validation failures behind generic success responses.

---

## 4. Inputs

| Artifact | Source |
| --- | --- |
| Objective definition | `.devflow/objective/o01-question-bank-v1.md` |
| Storage and validation layer | `o01/t02-build-question-storage-and-validation` |
| UI behavior expectations | `.devflow/context/ui-spec.md` |

---

## 5. Outputs

| Artifact | Path |
| --- | --- |
| Question Bank HTTP endpoints | `backend/` |
| API tests or integration tests | `tests/` |

---

## 6. Acceptance Criteria

> These criteria must all pass before the task is marked complete.

* [x] The app exposes endpoints that support question list, search, create, update, and delete flows.
* [x] Invalid inputs and missing-question cases return basic explicit error responses.
* [x] Automated tests cover the main API success and failure paths for V1.

---

## 7. Test Plan

```text
1. Start the local server.
2. Exercise each Question Bank endpoint manually or through automated tests.
3. Verify search filtering, create/update behavior, and delete behavior.
4. Verify invalid payloads and missing IDs return expected error responses.
```

---

## 8. Notes

Keep the API shape simple for plain JavaScript consumption.
