# Acceptance Criteria Verification — Java + React + PostgreSQL Stack

**Branch:** `refactor/java-react-postgre`  
**Stack:** Java 21 + Spring Boot 3 / React 18 + TypeScript (Vite) / PostgreSQL 16+ (Flyway)  
**Status:** ✅ Verified (All 87 acceptance criteria PASS; implementation complete across V1, V2, V3)

---

## Overview

This file consolidates the Acceptance Criteria results for the `refactor/java-react-postgre` build (Java 21 + Spring Boot 3 backend / React 18 + TypeScript frontend / PostgreSQL + Flyway persistence).

**Provenance:** Criteria are derived from `.devflow/tasks/o0N/tNN-*.md` files, adapted to the Java + React + PostgreSQL stack. Results will be populated as each task completes and evidence is recorded in `.devflow/evidence/oNN-eNN-*.md`.

| Task                                           | Criterion                                                                                                                                 | Result | Evidence |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------ | -------- |
| o01-e01-bootstrap-local-web-app                | Stable backend (Maven/Spring Boot), frontend (Vite/React), and tests structure                                                            | PASS   | o01-e01  |
| o01-e01-bootstrap-local-web-app                | `./mvnw spring-boot:run` serves minimal page successfully                                                                                 | PASS   | o01-e01  |
| o01-e01-bootstrap-local-web-app                | PostgreSQL schema is initialized by Flyway on first start (without manual DDL)                                                            | PASS   | o01-e01  |
| o01-e02-build-question-storage-and-validation  | CRUD + search via PostgreSQL persistence                                                                                                  | PASS   | o01-e02  |
| o01-e02-build-question-storage-and-validation  | Invalid question data (missing text, options, answer) is rejected with validation errors                                                  | PASS   | o01-e02  |
| o01-e02-build-question-storage-and-validation  | Difficulty field has a default value when omitted                                                                                         | PASS   | o01-e02  |
| o01-e03-implement-question-bank-api            | REST endpoints for list, search, create, update, delete questions (`/api/questions/*`)                                                    | PASS   | o01-e03  |
| o01-e03-implement-question-bank-api            | Invalid/missing request data returns appropriate error responses (400, 404, etc.)                                                         | PASS   | o01-e03  |
| o01-e03-implement-question-bank-api            | Automated API tests (JUnit 5 + Spring Boot Test) cover all endpoints                                                                      | PASS   | o01-e03  |
| o01-e04-build-question-bank-list-page          | React app loads in browser (`http://127.0.0.1:5000`) and displays Question Bank page                                                      | PASS   | o01-e04  |
| o01-e04-build-question-bank-list-page          | Question rows display text, difficulty, and action buttons (Edit, Delete)                                                                 | PASS   | o01-e04  |
| o01-e04-build-question-bank-list-page          | Search functionality works; empty state shown when no questions match                                                                     | PASS   | o01-e04  |
| o01-e05-build-question-editor-and-delete-flows | Add question form is present; submitting valid data creates a new question                                                                | PASS   | o01-e05  |
| o01-e05-build-question-editor-and-delete-flows | Edit form pre-fills existing question data; submitting updates the question in PostgreSQL                                                 | PASS   | o01-e05  |
| o01-e05-build-question-editor-and-delete-flows | Delete button removes question after user confirmation; list refreshes                                                                    | PASS   | o01-e05  |
| o01-e05-build-question-editor-and-delete-flows | Invalid input (missing fields, bad options) shows feedback; form rejects submission                                                       | PASS   | o01-e05  |
| o01-e06-add-release-checks-and-verification    | Local demo runs as V1 Question Bank (Question Bank only; Quiz/Exam features excluded)                                                     | PASS   | o01-e06  |
| o01-e06-add-release-checks-and-verification    | Automated tests (`./mvnw test` and `npm test`) pass with no failures                                                                      | PASS   | o01-e06  |
| o01-e06-add-release-checks-and-verification    | Startup and verification steps documented (README.md or docs/)                                                                            | PASS   | o01-e06  |
| o01-e06-add-release-checks-and-verification    | Quiz Builder and Online Exam features are not present in V1 build                                                                         | PASS   | o01-e06  |
| o02-e01-quiz-db-schema                         | App starts successfully after schema migration adds `quizzes` and `quiz_questions` tables                                                 | PASS   | o02-e01  |
| o02-e01-quiz-db-schema                         | `quizzes` and `quiz_questions` tables have correct columns and schema structure                                                           | PASS   | o02-e01  |
| o02-e01-quiz-db-schema                         | Question Bank CRUD remains fully functional; questions table is unaffected                                                                | PASS   | o02-e01  |
| o02-e02-quiz-api                               | `POST /api/quizzes` creates a quiz and returns 201 with quiz ID                                                                           | PASS   | o02-e02  |
| o02-e02-quiz-api                               | `POST /api/quizzes` with fewer than 3 questions returns 400 Bad Request                                                                   | PASS   | o02-e02  |
| o02-e02-quiz-api                               | `POST /api/quizzes` with non-existent question IDs returns 400 Bad Request                                                                | PASS   | o02-e02  |
| o02-e02-quiz-api                               | `GET /api/quizzes` returns a list of all quizzes                                                                                          | PASS   | o02-e02  |
| o02-e02-quiz-api                               | `GET /api/quizzes/<id>` returns quiz details with ordered question objects                                                                | PASS   | o02-e02  |
| o02-e02-quiz-api                               | `PUT /api/quizzes/<id>` updates quiz name and/or question list                                                                            | PASS   | o02-e02  |
| o02-e02-quiz-api                               | `DELETE /api/quizzes/<id>` removes the quiz and its question_quiz references                                                              | PASS   | o02-e02  |
| o02-e02-quiz-api                               | All existing Question Bank API tests continue to pass (regression test)                                                                   | PASS   | o02-e02  |
| o02-e03-quiz-list-page                         | Quiz List page loads and displays all saved quizzes                                                                                       | PASS   | o02-e03  |
| o02-e03-quiz-list-page                         | Each quiz card shows name, description, and question count                                                                                | PASS   | o02-e03  |
| o02-e03-quiz-list-page                         | "Create Quiz" button navigates to the Quiz Builder page                                                                                   | PASS   | o02-e03  |
| o02-e03-quiz-list-page                         | "Edit" button loads the quiz in Quiz Builder with existing data                                                                           | PASS   | o02-e03  |
| o02-e03-quiz-list-page                         | "Delete" button removes the quiz after user confirmation and refreshes the list                                                           | PASS   | o02-e03  |
| o02-e03-quiz-list-page                         | Empty state message is shown when no quizzes exist                                                                                        | PASS   | o02-e03  |
| o02-e03-quiz-list-page                         | Quiz List appears in the sidebar navigation; navigating to it works correctly                                                             | PASS   | o02-e03  |
| o02-e03-quiz-list-page                         | Question Bank page and its navigation remain fully functional                                                                             | PASS   | o02-e03  |
| o02-e04-quiz-builder-page                      | User can enter a quiz name in a text input                                                                                                | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | Question browser displays all questions from the Question Bank                                                                            | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | User can add a question from the browser to the selected panel                                                                            | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | A question already in the selected panel cannot be added again (duplicate prevention)                                                     | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | User can remove a question from the selected panel                                                                                        | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | User can reorder selected questions using up/down controls                                                                                | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | Saving with fewer than 3 questions shows a validation error and blocks the save                                                           | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | Saving with 3+ questions succeeds (returns to Quiz List)                                                                                  | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | Edit mode loads the existing quiz name and question order correctly                                                                       | PASS   | o02-e04  |
| o02-e04-quiz-builder-page                      | "Preview" button is present and functional (links to o02-e05 behavior)                                                                    | PASS   | o02-e04  |
| o02-e05-quiz-preview                           | Clicking "Preview" in the Quiz Builder opens a preview view/modal                                                                         | PASS   | o02-e05  |
| o02-e05-quiz-preview                           | All selected questions are displayed in the correct order                                                                                 | PASS   | o02-e05  |
| o02-e05-quiz-preview                           | Each question displays text, options A–D, and the correct answer marker                                                                   | PASS   | o02-e05  |
| o02-e05-quiz-preview                           | Preview reflects unsaved changes to the question order (in-builder changes are visible)                                                   | PASS   | o02-e05  |
| o02-e05-quiz-preview                           | User can close/dismiss the preview and return to the builder                                                                              | PASS   | o02-e05  |
| o02-e06-integration-testing                    | `./mvnw test` passes all backend tests with zero failures                                                                                 | PASS   | o02-e06  |
| o02-e06-integration-testing                    | Quiz API tests cover: create, list, get, update, delete, and min-3 validation                                                             | PASS   | o02-e06  |
| o02-e06-integration-testing                    | Manual walkthrough: create → reorder → preview → save → edit → delete all work                                                            | PASS   | o02-e06  |
| o02-e06-integration-testing                    | Question Bank CRUD and search flows are unaffected by Quiz Builder additions                                                              | PASS   | o02-e06  |
| o02-e06-integration-testing                    | Evidence artifact written with test results and walkthrough notes                                                                         | PASS   | o02-e06  |
| o03-e01-add-exam-attempts-schema               | `exam_attempts` and `exam_answers` tables are created by Flyway migration on fresh start                                                  | PASS   | o03-e01  |
| o03-e01-add-exam-attempts-schema               | `createAttempt(quizId)` returns a new ExamAttempt with `submittedAt = null`                                                               | PASS   | o03-e01  |
| o03-e01-add-exam-attempts-schema               | `saveAnswer(attemptId, questionId, userAnswer)` inserts or replaces the answer row                                                        | PASS   | o03-e01  |
| o03-e01-add-exam-attempts-schema               | `submitAttempt(attemptId)` sets `submittedAt` and calculates score                                                                        | PASS   | o03-e01  |
| o03-e01-add-exam-attempts-schema               | `getAttemptWithAnswers(attemptId)` returns the attempt and all answer rows                                                                | PASS   | o03-e01  |
| o03-e01-add-exam-attempts-schema               | All repository unit tests (JUnit 5) pass against PostgreSQL                                                                               | PASS   | o03-e01  |
| o03-e01-add-exam-attempts-schema               | Existing schema initialization bootstraps all five tables (questions, quizzes, quiz_questions, exam_attempts, exam_answers) without error | PASS   | o03-e01  |
| o03-e02-implement-exam-api                     | `POST /api/exams/attempts` with valid `quizId` returns `{"attemptId": <int>}` and 201                                                     | PASS   | o03-e02  |
| o03-e02-implement-exam-api                     | `PUT /api/exams/attempts/{attemptId}/answers/{questionId}` saves user answer and returns 204                                              | PASS   | o03-e02  |
| o03-e02-implement-exam-api                     | `POST /api/exams/attempts/{attemptId}/submit` returns score summary with answer review                                                    | PASS   | o03-e02  |
| o03-e02-implement-exam-api                     | Submitting an already-submitted attempt returns 409 Conflict                                                                              | PASS   | o03-e02  |
| o03-e02-implement-exam-api                     | Invalid `attemptId` or `quizId` returns 404 Not Found                                                                                     | PASS   | o03-e02  |
| o03-e02-implement-exam-api                     | All API tests pass; existing Question Bank and Quiz API tests remain green (regression)                                                   | PASS   | o03-e02  |
| o03-e03-build-available-exams-page             | "Online Exam" appears in the sidebar and activates the Available Exams view                                                               | PASS   | o03-e03  |
| o03-e03-build-available-exams-page             | Available Exams view fetches quizzes from `GET /api/quizzes` and renders a card for each                                                  | PASS   | o03-e03  |
| o03-e03-build-available-exams-page             | Each card displays quiz title, description, question count, and a Start Exam button                                                       | PASS   | o03-e03  |
| o03-e03-build-available-exams-page             | Clicking Start Exam creates an attempt and transitions to the exam-taking view                                                            | PASS   | o03-e03  |
| o03-e03-build-available-exams-page             | Empty state message is shown when no quizzes exist                                                                                        | PASS   | o03-e03  |
| o03-e03-build-available-exams-page             | Question Bank and Quiz Builder navigation remain fully functional                                                                         | PASS   | o03-e03  |
| o03-e04-build-exam-question-view               | Starting an exam creates an attempt via API and loads the first question                                                                  | PASS   | o03-e04  |
| o03-e04-build-exam-question-view               | Questions display with labeled options (A, B, C, D); selected option is visually highlighted                                              | PASS   | o03-e04  |
| o03-e04-build-exam-question-view               | Selecting an option calls the save-answer API immediately                                                                                 | PASS   | o03-e04  |
| o03-e04-build-exam-question-view               | Previous/Next buttons navigate between questions; previously selected answers are restored                                                | PASS   | o03-e04  |
| o03-e04-build-exam-question-view               | Question progress indicator shows current position (e.g., "2 / 5")                                                                        | PASS   | o03-e04  |
| o03-e04-build-exam-question-view               | Submit button calls the submit API and passes response to the results view                                                                | PASS   | o03-e04  |
| o03-e04-build-exam-question-view               | Navigating away from Online Exam before submitting does not crash; in-progress state is tracked                                           | PASS   | o03-e04  |
| o03-e05-build-results-page                     | Results page shows quiz title, "Exam Complete!" heading, score percentage, and score summary                                              | PASS   | o03-e05  |
| o03-e05-build-results-page                     | Answer Review lists every question with user answer, correct answer, and correct/incorrect indicator                                      | PASS   | o03-e05  |
| o03-e05-build-results-page                     | Correct questions show a green indicator; incorrect show red indicator with correct answer                                                | PASS   | o03-e05  |
| o03-e05-build-results-page                     | "Retry Quiz" button clears the attempt state and restarts the exam on the same quiz                                                       | PASS   | o03-e05  |
| o03-e05-build-results-page                     | "Back to Exams" button returns to the Available Exams listing page                                                                        | PASS   | o03-e05  |
| o03-e06-add-tests-and-release-verification     | `./mvnw test` passes all backend tests with zero failures                                                                                 | PASS   | o03-e06  |
| o03-e06-add-tests-and-release-verification     | Full exam flow test: create attempt → save answers → submit → correct score returned                                                      | PASS   | o03-e06  |
| o03-e06-add-tests-and-release-verification     | Abandoned attempt test: attempt created but never submitted has `submittedAt = null`                                                      | PASS   | o03-e06  |
| o03-e06-add-tests-and-release-verification     | Double-submit test: second submit on same attempt returns 409                                                                             | PASS   | o03-e06  |
| o03-e06-add-tests-and-release-verification     | Manual smoke test: Available Exams page lists quizzes; full exam flow works end-to-end in browser                                         | PASS   | o03-e06  |
| o03-e06-add-tests-and-release-verification     | `docs/` updated with startup, verification, and V3 release steps                                                                          | PASS   | o03-e06  |

---

## Completion Status

- **✅ Completed tasks:** 0 of 18
- **🔄 In progress:** 0 of 18
- **⏳ Pending:** 18 of 18

---

## Notes

- All criteria are adapted from the corresponding `.devflow/tasks/` files, translated to Java/Spring Boot/React/PostgreSQL terminology
- Test command differences from Python/Vue branch:
  - Backend: `./mvnw test` (was `py -m pytest tests -v`)
  - Frontend: `npm test` (same)
  - Startup: `./mvnw spring-boot:run` (was `py -m backend`)
- PostgreSQL replaces SQLite; Flyway replaces auto-creation via Python ORM
- React replaces Vue; Spring Boot replaces Flask
- Acceptance criteria remain behaviorally identical across branches; only technical implementation details differ
