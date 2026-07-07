# Task: Quiz Database Schema

**ID:** o02/t01-quiz-db-schema
**File:** `.devflow/tasks/o02/t01-quiz-db-schema.md`
**Objective Ref:** `.devflow/objective/o02-quiz-builder-v1.md`
**Depends On:** none
**Complexity:** S
**Estimated Duration:** 30 min
**Status:** verified

---

## 1. Purpose

Extend the SQLite database with two new tables — `quizzes` and `quiz_questions` — to support quiz storage and ordered question references. After this task, the persistence layer is ready for the Quiz API to build on.

---

## 2. Boundary

### In Scope

- Create `quizzes` table: `id`, `name`, `created_at`
- Create `quiz_questions` join table: `quiz_id`, `question_id`, `position`
- Add schema migration logic consistent with the existing migration pattern
- Ensure migration runs on app startup without affecting existing tables

### Out of Scope

- API endpoints (t02)
- Any frontend changes
- Modifications to the `questions` table or existing migration versions

---

## 3. Must / Must Not

### Must

- Use a new migration version that runs after the existing schema
- `quiz_questions.position` must be an integer used to preserve manual ordering
- Foreign key from `quiz_questions.question_id` to `questions.id` must be defined
- Foreign key from `quiz_questions.quiz_id` to `quizzes.id` must be defined

### Must Not

- Alter or drop any existing table
- Store question content in `quiz_questions`; store only the reference ID

---

## 4. Inputs

| Artifact                   | Source                        |
| -------------------------- | ----------------------------- |
| Existing migration pattern | `backend/` database bootstrap |

---

## 5. Outputs

| Artifact                          | Path       |
| --------------------------------- | ---------- |
| Updated database bootstrap module | `backend/` |

---

## 6. Acceptance Criteria

- [x] App starts without errors after schema change
- [x] `quizzes` table exists with `id`, `name`, `created_at` columns
- [x] `quiz_questions` table exists with `quiz_id`, `question_id`, `position` columns
- [x] Existing `questions` table and data are unaffected

---

## 7. Test Plan

```
py -m pytest tests/ -v
# verify existing tests still pass
# manually inspect schema via SQLite if needed
```

---

## 8. Notes

Follow the existing versioned migration pattern in the backend. Do not use a migration library; keep it consistent with the current approach.
