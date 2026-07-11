# Acceptance Criteria Verification (Merged)

This file consolidates the Acceptance Criteria results from every evidence artifact in `.devflow/evidence/*.md` (the `rebuild/codex` build) into a single table.

| Task                                           | Criterion                                                                                                          | Result |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------ |
| o01-e01-bootstrap-local-web-app                | The repository has a stable local app structure for backend, frontend, and tests.                                  | PASS   |
| o01-e01-bootstrap-local-web-app                | The application can be started by a Python command and serve at least a minimal page successfully.                 | PASS   |
| o01-e01-bootstrap-local-web-app                | SQLite initialization runs on first start without requiring manual database setup.                                 | PASS   |
| o01-e02-build-question-storage-and-validation  | Questions can be inserted, updated, deleted, listed, and searched through the persistence layer.                   | PASS   |
| o01-e02-build-question-storage-and-validation  | Invalid question data is rejected according to the V1 validation rules.                                            | PASS   |
| o01-e02-build-question-storage-and-validation  | Difficulty receives a default value when omitted.                                                                  | PASS   |
| o01-e03-implement-question-bank-api            | The app exposes endpoints that support question list, search, create, update, and delete flows.                    | PASS   |
| o01-e03-implement-question-bank-api            | Invalid inputs and missing-question cases return basic explicit error responses.                                   | PASS   |
| o01-e03-implement-question-bank-api            | Automated tests cover the main API success and failure paths for V1.                                               | PASS   |
| o01-e04-build-question-bank-list-page          | Users can open the local app and view the Question Bank page in the browser.                                       | PASS   |
| o01-e04-build-question-bank-list-page          | The page renders question rows with text, difficulty, and visible actions.                                         | PASS   |
| o01-e04-build-question-bank-list-page          | Search updates the visible list and shows the empty state correctly when no matches exist.                         | PASS   |
| o01-e05-build-question-editor-and-delete-flows | Users can add a new question through the UI and see it appear in the list.                                         | PASS   |
| o01-e05-build-question-editor-and-delete-flows | Users can edit an existing question and see updates reflected in the list.                                         | PASS   |
| o01-e05-build-question-editor-and-delete-flows | Users can delete a question through a confirmation dialog and see it removed from the list.                        | PASS   |
| o01-e05-build-question-editor-and-delete-flows | Invalid question input is blocked and surfaced to the user with basic error feedback.                              | PASS   |
| o01-e06-add-release-checks-and-verification    | The application can be started locally and demonstrated as a V1 Question Bank web app.                             | PASS   |
| o01-e06-add-release-checks-and-verification    | Automated tests cover the basic V1 backend and/or integration baseline.                                            | PASS   |
| o01-e06-add-release-checks-and-verification    | Local run and verification steps are documented clearly enough for a fresh user or AI session.                     | PASS   |
| o01-e06-add-release-checks-and-verification    | The final V1 build still excludes Quiz Builder and Online Exam functionality.                                      | PASS   |
| o02-e01-quiz-db-schema                         | App starts without errors after schema change                                                                      | PASS   |
| o02-e01-quiz-db-schema                         | `quizzes` table exists with `id`, `name`, `created_at` columns                                                     | PASS   |
| o02-e01-quiz-db-schema                         | `quiz_questions` table exists with `quiz_id`, `question_id`, `position` columns                                    | PASS   |
| o02-e01-quiz-db-schema                         | Existing `questions` table and data are unaffected                                                                 | PASS   |
| o02-e02-quiz-api                               | `POST /api/quizzes` creates a quiz and returns 201                                                                 | PASS   |
| o02-e02-quiz-api                               | `POST /api/quizzes` with fewer than 3 questions returns 400                                                        | PASS   |
| o02-e02-quiz-api                               | `POST /api/quizzes` with a non-existent question ID returns 400                                                    | PASS   |
| o02-e02-quiz-api                               | `GET /api/quizzes` returns a list of quizzes                                                                       | PASS   |
| o02-e02-quiz-api                               | `GET /api/quizzes/<id>` returns quiz details including ordered question objects                                    | PASS   |
| o02-e02-quiz-api                               | `PUT /api/quizzes/<id>` updates name and/or question list                                                          | PASS   |
| o02-e02-quiz-api                               | `DELETE /api/quizzes/<id>` removes the quiz and its question references                                            | PASS   |
| o02-e02-quiz-api                               | All existing Question Bank API tests continue to pass                                                              | PASS   |
| o02-e03-quiz-list-page                         | Quiz List page loads and displays all saved quizzes                                                                | PASS   |
| o02-e03-quiz-list-page                         | Each quiz entry shows its name and question count                                                                  | PASS   |
| o02-e03-quiz-list-page                         | "Create Quiz" button navigates to the Quiz Builder page                                                            | PASS   |
| o02-e03-quiz-list-page                         | "Edit" button navigates to the Quiz Builder with the correct quiz loaded                                           | PASS   |
| o02-e03-quiz-list-page                         | "Delete" button removes the quiz after confirmation and refreshes the list                                         | PASS   |
| o02-e03-quiz-list-page                         | Empty state message is shown when no quizzes exist                                                                 | PASS   |
| o02-e03-quiz-list-page                         | Navigation includes a link to the Quiz List page                                                                   | PASS   |
| o02-e03-quiz-list-page                         | Question Bank page and navigation are unaffected                                                                   | PASS   |
| o02-e04-quiz-builder-page                      | User can enter a quiz name                                                                                         | PASS   |
| o02-e04-quiz-builder-page                      | Question browser shows all questions from the Question Bank                                                        | PASS   |
| o02-e04-quiz-builder-page                      | User can add a question to the selected panel                                                                      | PASS   |
| o02-e04-quiz-builder-page                      | A question already selected cannot be added again                                                                  | PASS   |
| o02-e04-quiz-builder-page                      | User can remove a question from the selected panel                                                                 | PASS   |
| o02-e04-quiz-builder-page                      | User can reorder selected questions using up/down controls                                                         | PASS   |
| o02-e04-quiz-builder-page                      | Saving with fewer than 3 questions is blocked with a visible error message                                         | PASS   |
| o02-e04-quiz-builder-page                      | Saving with 3 or more questions succeeds and returns to the Quiz List                                              | PASS   |
| o02-e04-quiz-builder-page                      | Edit mode loads the existing quiz name and question order correctly                                                | PASS   |
| o02-e04-quiz-builder-page                      | "Preview" button is present and functional (links to t05 behavior)                                                 | PASS   |
| o02-e05-quiz-preview                           | Clicking "Preview" in the Quiz Builder opens the preview                                                           | PASS   |
| o02-e05-quiz-preview                           | All selected questions are shown in order                                                                          | PASS   |
| o02-e05-quiz-preview                           | Each question displays text, options A-D, and the correct answer                                                   | PASS   |
| o02-e05-quiz-preview                           | Preview reflects the current in-builder question order (including unsaved changes)                                 | PASS   |
| o02-e05-quiz-preview                           | User can close/dismiss the preview and return to the builder                                                       | PASS   |
| o02-e06-integration-testing                    | `py -m pytest tests/ -v` passes with no failures                                                                   | PASS   |
| o02-e06-integration-testing                    | Quiz API tests cover: create, list, get, update, delete, and the min-3 validation rejection                        | PASS   |
| o02-e06-integration-testing                    | Manual walkthrough completed: create -> reorder -> preview -> save -> edit -> delete                               | PASS   |
| o02-e06-integration-testing                    | Question Bank CRUD and search flows are unaffected                                                                 | PASS   |
| o02-e06-integration-testing                    | Evidence artifact written with test results and walkthrough notes                                                  | PASS   |
| o03-e01-add-exam-attempts-schema               | `exam_attempts` and `exam_answers` tables are created by the migration on a fresh database                         | PASS   |
| o03-e01-add-exam-attempts-schema               | `create_attempt(quiz_id)` returns a new attempt with `submitted_at = NULL`                                         | PASS   |
| o03-e01-add-exam-attempts-schema               | `save_answer(attempt_id, question_id, selected_option)` inserts or replaces the answer row                         | PASS   |
| o03-e01-add-exam-attempts-schema               | `submit_attempt(attempt_id, score, total)` sets `submitted_at` and `score`                                         | PASS   |
| o03-e01-add-exam-attempts-schema               | `get_attempt_with_answers(attempt_id)` returns the attempt and all its answer rows                                 | PASS   |
| o03-e01-add-exam-attempts-schema               | All repository unit tests pass against a temporary in-memory database                                              | PASS   |
| o03-e01-add-exam-attempts-schema               | Existing `initialize_database()` call still bootstraps all tables without error                                    | PASS   |
| o03-e02-implement-exam-api                     | `POST /api/exams/attempts` with a valid `quiz_id` returns `{"attempt_id": <int>}` and 201                          | PASS   |
| o03-e02-implement-exam-api                     | `PUT /api/exams/attempts/{attempt_id}/answers/{question_id}` with `{"selected_option": "A"}` returns 204           | PASS   |
| o03-e02-implement-exam-api                     | Submit returns `{score, total, percentage, answers[...]}` with answer review data                                  | PASS   |
| o03-e02-implement-exam-api                     | Submitting an already submitted attempt returns 409                                                                | PASS   |
| o03-e02-implement-exam-api                     | Invalid `attempt_id` or `quiz_id` returns 404                                                                      | PASS   |
| o03-e02-implement-exam-api                     | Exam API tests and existing regression suite remain green                                                          | PASS   |
| o03-e03-build-available-exams-page             | "Online Exam" appears in the sidebar and activates the Available Exams view                                        | PASS   |
| o03-e03-build-available-exams-page             | Available Exams view fetches quizzes from `GET /api/quizzes` and renders a card for each                           | PASS   |
| o03-e03-build-available-exams-page             | Each card shows quiz title, description, question count, and Start Exam button                                     | PASS   |
| o03-e03-build-available-exams-page             | Start Exam transitions the UI toward the in-exam view and stores selected quiz context                             | PASS   |
| o03-e03-build-available-exams-page             | Empty state is shown when no quizzes exist                                                                         | PASS   |
| o03-e03-build-available-exams-page             | Question Bank and Quiz Builder navigation remain functional                                                        | PASS   |
| o03-e04-build-exam-question-view               | Starting an exam creates an attempt via API and loads the first question                                           | PASS   |
| o03-e04-build-exam-question-view               | Questions display with labeled options and selected option highlighting                                            | PASS   |
| o03-e04-build-exam-question-view               | Selecting an option calls the save-answer API immediately                                                          | PASS   |
| o03-e04-build-exam-question-view               | Previous and Next navigation restore saved answers                                                                 | PASS   |
| o03-e04-build-exam-question-view               | Question progress indicator shows current position                                                                 | PASS   |
| o03-e04-build-exam-question-view               | Submit calls the submit API and passes response payload to results view                                            | PASS   |
| o03-e04-build-exam-question-view               | Navigating away before submitting does not crash the app                                                           | PASS   |
| o03-e05-build-results-page                     | Results page shows quiz title, completion heading, score percentage, correct count, and incorrect count            | PASS   |
| o03-e05-build-results-page                     | Answer Review lists every question with question text, user's answer, correct answer when different, and indicator | PASS   |
| o03-e05-build-results-page                     | Correct questions show green styling; incorrect questions show red styling with correct answer highlighted         | PASS   |
| o03-e05-build-results-page                     | Retry Quiz clears the current attempt and restarts the exam on the same quiz                                       | PASS   |
| o03-e05-build-results-page                     | Back to Exams returns to the Available Exams listing page                                                          | PASS   |
| o03-e06-add-tests-and-release-verification     | `pytest tests/ -v` passes with zero failures                                                                       | PASS   |
| o03-e06-add-tests-and-release-verification     | Full exam flow test covers create attempt, save answers, submit, and score verification                            | PASS   |
| o03-e06-add-tests-and-release-verification     | Abandoned attempt remains unsubmitted with `submitted_at = NULL`                                                   | PASS   |
| o03-e06-add-tests-and-release-verification     | Double-submit returns 409                                                                                          | PASS   |
| o03-e06-add-tests-and-release-verification     | Manual smoke steps for Online Exam are documented                                                                  | PASS   |
| o03-e06-add-tests-and-release-verification     | Existing V1 and V2 tests remain green                                                                              | PASS   |
