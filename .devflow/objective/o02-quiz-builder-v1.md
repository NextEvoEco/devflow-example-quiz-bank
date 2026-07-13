# Objective: Quiz Builder V1

**ID:** o02-quiz-builder-v1
**Version:** V1
**Date:** 2026-06-28
**Status:** ready
**Interview Ref:** `.devflow/interview/i02-quiz-builder.md`

---

## 1. Goal

Allow users to compose reusable quizzes by selecting and ordering questions from the existing Question Bank.

This version introduces quiz creation, management, manual reordering of selected questions, a minimum-question validation rule, and a full-quiz preview — without modifying any existing Question Bank behavior.

---

## 2. Background

The Question Bank V1 established a reusable library of questions. The next product step is to let users organize those questions into named quizzes that can later be used in Online Exam scenarios. Keeping quiz management separate from question management preserves a clean module boundary and prepares the codebase for future expansion.

---

## 3. Scope

### In Scope

- Quiz data model: name, ordered question references, creation timestamp
- Quiz CRUD: create, read, update, delete
- Question selection from the existing Question Bank (by reference, no duplication)
- Manual reordering of questions within a quiz
- Validation: minimum 3 questions required to save
- Quiz preview: display full quiz content (question text, options, correct answer)
- Quiz list page: browse and manage saved quizzes

### Out of Scope

- Quiz metadata beyond name (description, tags, difficulty)
- Maximum question count limit
- Random question order / shuffle setting
- Online Exam execution runtime
- Modifications to the Question Bank module
- Multi-type quiz support

---

## 4. Constraints

| Type       | Constraint                                                                 |
| ---------- | -------------------------------------------------------------------------- |
| Platform   | Local web application                                                      |
| Tech Stack | Java 21 + Spring Boot 3, PostgreSQL (Flyway), React 18 + TypeScript (Vite) |
| Scope      | Question Bank module must remain unchanged                                 |
| Data       | Questions are referenced by ID; no duplication in storage                  |
| Validation | Quiz requires at least 3 questions to be saveable                          |
| UI         | Follow approved application layout and navigation                          |

---

## 5. Success Criteria

- [ ] User can create a quiz with a name and at least 3 selected questions
- [ ] User can browse and select questions from the Question Bank when building a quiz
- [ ] User can manually reorder selected questions within the quiz
- [ ] Saving a quiz with fewer than 3 questions is rejected with a clear error message
- [ ] User can preview the full quiz content (question text, options, correct answer) before saving
- [ ] User can view a list of all saved quizzes
- [ ] User can edit an existing quiz (rename, add/remove/reorder questions)
- [ ] User can delete a quiz
- [ ] All existing Question Bank behavior continues to work without regression

---

## 6. Open Questions

| #   | Question                                      | Owner | Status                                     |
| --- | --------------------------------------------- | ----- | ------------------------------------------ |
| 1   | Storage model for quiz-question relationships | AI    | resolved — join table with position column |

---

## 7. Confirmation

**Confirmed by:** user
**Confirmed at:** 2026-06-28

> Proceed with task splitting.
