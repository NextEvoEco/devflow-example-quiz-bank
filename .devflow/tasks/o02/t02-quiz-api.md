# Task: Quiz CRUD API

**ID:** o02/t02-quiz-api
**File:** `.devflow/tasks/o02/t02-quiz-api.md`
**Objective Ref:** `.devflow/objective/o02-quiz-builder-v1.md`
**Depends On:** o02/t01-quiz-db-schema
**Complexity:** M
**Estimated Duration:** 1.5 hr
**Status:** verified

---

## 1. Purpose

Implement the backend API layer for quiz management. After this task, the frontend can create, retrieve, update, delete quizzes, and manage their ordered question lists through HTTP endpoints.

---

## 2. Boundary

### In Scope

- `GET /api/quizzes` — list all quizzes (id, name, question count)
- `POST /api/quizzes` — create a quiz (name + ordered question IDs)
- `GET /api/quizzes/<id>` — get a single quiz with full question details
- `PUT /api/quizzes/<id>` — update quiz name and/or question list
- `DELETE /api/quizzes/<id>` — delete a quiz and its question references
- Validation: reject save if fewer than 3 questions
- Repository class for quiz data access (consistent with `QuestionRepository` pattern)

### Out of Scope

- Frontend (t03–t05)
- Question Bank endpoints — must not be modified
- Exam execution endpoints

---

## 3. Must / Must Not

### Must

- Return a 400 error with a descriptive message when fewer than 3 questions are provided on create or update
- Store `position` values from the request to preserve question order
- Question references must be validated: all provided question IDs must exist in the `questions` table
- Follow the same Flask blueprint and repository pattern used by the Question Bank

### Must Not

- Modify any existing Question Bank routes or repository
- Duplicate question data — store IDs only
- Accept a quiz with duplicate question IDs in the same quiz

---

## 4. Inputs

| Artifact              | Source                 |
| --------------------- | ---------------------- |
| DB schema (t01)       | o02/t01-quiz-db-schema |
| QuestionRepository    | `backend/`             |
| Existing Flask routes | `backend/`             |

---

## 5. Outputs

| Artifact               | Path       |
| ---------------------- | ---------- |
| Quiz repository module | `backend/` |
| Quiz routes module     | `backend/` |

---

## 6. Acceptance Criteria

- [x] `POST /api/quizzes` creates a quiz and returns 201
- [x] `POST /api/quizzes` with fewer than 3 questions returns 400
- [x] `POST /api/quizzes` with a non-existent question ID returns 400
- [x] `GET /api/quizzes` returns a list of quizzes
- [x] `GET /api/quizzes/<id>` returns quiz details including ordered question objects
- [x] `PUT /api/quizzes/<id>` updates name and/or question list
- [x] `DELETE /api/quizzes/<id>` removes the quiz and its question references
- [x] All existing Question Bank API tests continue to pass

---

## 7. Test Plan

```
py -m pytest tests/ -v
# also manually test with curl or browser devtools after t03 is available
```

---

## 8. Notes

The `GET /api/quizzes/<id>` response should include full question objects (text, options, correct answer) to support the preview feature in t05 without an additional API call.
