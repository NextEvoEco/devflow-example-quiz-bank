# Acceptance Criteria Verification (Merged)

This file consolidates the Acceptance Criteria results from every evidence artifact in `.devflow/evidence/*.md` (the `rebuild/cursor` build) into a single table.

| Task                                           | Criterion                                                                                      | Result  |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------- |
| o01-e01-bootstrap-local-web-app                | Stable local app structure for backend, frontend, and tests                                    | PASS    |
| o01-e01-bootstrap-local-web-app                | Application starts via Python command and serves a minimal page                                | PASS    |
| o01-e01-bootstrap-local-web-app                | SQLite initialization runs on first start without manual setup                                 | PASS    |
| o01-e02-build-question-storage-and-validation  | Questions can be inserted, updated, deleted, listed, and searched                              | PASS    |
| o01-e02-build-question-storage-and-validation  | Invalid question data is rejected with validation rules                                        | PASS    |
| o01-e02-build-question-storage-and-validation  | Difficulty receives a default value when omitted                                               | PASS    |
| o01-e03-implement-question-bank-api            | The app exposes endpoints that support question list, search, create, update, and delete flows | PARTIAL |
| o01-e03-implement-question-bank-api            | Invalid inputs and missing-question cases return basic explicit error responses                | PARTIAL |
| o01-e03-implement-question-bank-api            | Automated tests cover the main API success and failure paths for V1                            | PASS    |
| o01-e04-build-question-bank-list-page          | Users can open the app and view the Question Bank page                                         | PASS    |
| o01-e04-build-question-bank-list-page          | Page renders rows with text, difficulty, and visible actions                                   | PASS    |
| o01-e04-build-question-bank-list-page          | Search updates list and shows empty state correctly                                            | PASS    |
| o01-e05-build-question-editor-and-delete-flows | Users can add a new question and see it in the list                                            | PASS    |
| o01-e05-build-question-editor-and-delete-flows | Users can edit an existing question and see updates                                            | PASS    |
| o01-e05-build-question-editor-and-delete-flows | Users can delete through confirmation and see removal                                          | PASS    |
| o01-e05-build-question-editor-and-delete-flows | Invalid input is blocked with basic error feedback                                             | PASS    |
| o01-e06-add-release-checks-and-verification    | App starts locally and demonstrates V1 Question Bank                                           | PASS    |
| o01-e06-add-release-checks-and-verification    | Automated tests cover V1 baseline                                                              | PASS    |
| o01-e06-add-release-checks-and-verification    | Run/verification steps documented                                                              | PASS    |
| o01-e06-add-release-checks-and-verification    | Out-of-scope features excluded                                                                 | PASS    |
| o02-e01-quiz-db-schema                         | App starts without errors after schema change                                                  | PASS    |
| o02-e01-quiz-db-schema                         | `quizzes` table exists with required columns                                                   | PASS    |
| o02-e01-quiz-db-schema                         | `quiz_questions` table exists with required columns                                            | PASS    |
| o02-e01-quiz-db-schema                         | Existing `questions` table unaffected                                                          | PASS    |
| o02-e02-quiz-api                               | POST creates quiz (201)                                                                        | PASS    |
| o02-e02-quiz-api                               | POST with <3 questions returns 400                                                             | PASS    |
| o02-e02-quiz-api                               | POST with missing question ID returns 400                                                      | PASS    |
| o02-e02-quiz-api                               | GET list returns quizzes                                                                       | PASS    |
| o02-e02-quiz-api                               | GET by id returns ordered questions                                                            | PASS    |
| o02-e02-quiz-api                               | PUT updates name/questions                                                                     | PASS    |
| o02-e02-quiz-api                               | DELETE removes quiz                                                                            | PASS    |
| o02-e02-quiz-api                               | Question Bank tests still pass                                                                 | PASS    |
| o02-e03-quiz-list-page                         | Quiz List page loads and displays saved quizzes                                                | PASS    |
| o02-e03-quiz-list-page                         | Each quiz entry shows name and question count                                                  | PASS    |
| o02-e03-quiz-list-page                         | Create Quiz button navigates to Quiz Builder page                                              | PASS    |
| o02-e03-quiz-list-page                         | Edit button navigates to Quiz Builder with correct quiz loaded                                 | PASS    |
| o02-e03-quiz-list-page                         | Delete button removes quiz and refreshes list                                                  | PASS    |
| o02-e03-quiz-list-page                         | Empty state shown when no quizzes exist                                                        | PASS    |
| o02-e03-quiz-list-page                         | Navigation includes Quiz List link                                                             | PASS    |
| o02-e03-quiz-list-page                         | Question Bank page and navigation unaffected                                                   | PASS    |
| o02-e04-quiz-builder-page                      | Quiz name input                                                                                | PASS    |
| o02-e04-quiz-builder-page                      | Question browser shows bank questions                                                          | PASS    |
| o02-e04-quiz-builder-page                      | Add/remove/reorder selected questions                                                          | PASS    |
| o02-e04-quiz-builder-page                      | Duplicate selection prevented                                                                  | PASS    |
| o02-e04-quiz-builder-page                      | Save blocked below 3 questions                                                                 | PASS    |
| o02-e04-quiz-builder-page                      | Save succeeds with 3+ questions                                                                | PASS    |
| o02-e04-quiz-builder-page                      | Edit mode loads existing quiz                                                                  | PASS    |
| o02-e04-quiz-builder-page                      | Preview button present                                                                         | PASS    |
| o02-e05-quiz-preview                           | Preview opens from Quiz Builder                                                                | PASS    |
| o02-e05-quiz-preview                           | Questions shown in order                                                                       | PASS    |
| o02-e05-quiz-preview                           | Each question shows text, options, correct answer                                              | PASS    |
| o02-e05-quiz-preview                           | Reflects unsaved builder order                                                                 | PASS    |
| o02-e05-quiz-preview                           | User can dismiss and return to builder                                                         | PASS    |
| o02-e06-integration-testing                    | `py -m pytest tests/ -v` passes                                                                | PASS    |
| o02-e06-integration-testing                    | Quiz API tests cover CRUD + min-3 validation                                                   | PASS    |
| o02-e06-integration-testing                    | Manual walkthrough documented                                                                  | PASS    |
| o02-e06-integration-testing                    | Question Bank unaffected                                                                       | PASS    |
| o02-e06-integration-testing                    | Evidence artifact written                                                                      | PASS    |
| o03-e01-add-exam-attempts-schema               | Tables created on fresh database                                                               | PASS    |
| o03-e01-add-exam-attempts-schema               | `create_attempt` returns pending attempt                                                       | PASS    |
| o03-e01-add-exam-attempts-schema               | `save_answer` inserts/replaces                                                                 | PASS    |
| o03-e01-add-exam-attempts-schema               | `submit_attempt` sets score and timestamp                                                      | PASS    |
| o03-e01-add-exam-attempts-schema               | `get_attempt_with_answers` returns full record                                                 | PASS    |
| o03-e01-add-exam-attempts-schema               | Repository unit tests pass                                                                     | PASS    |
| o03-e01-add-exam-attempts-schema               | `init_database()` still bootstraps cleanly                                                     | PASS    |
| o03-e02-implement-exam-api                     | Create attempt returns 201 + attempt_id                                                        | PASS    |
| o03-e02-implement-exam-api                     | Save answer returns 204                                                                        | PASS    |
| o03-e02-implement-exam-api                     | Submit returns score summary with answer review                                                | PASS    |
| o03-e02-implement-exam-api                     | Resubmit returns 409                                                                           | PASS    |
| o03-e02-implement-exam-api                     | Invalid quiz/attempt returns 404                                                               | PASS    |
| o03-e02-implement-exam-api                     | Full regression green                                                                          | PASS    |
| o03-e03-build-available-exams-page             | Online Exam nav activates Available Exams view                                                 | PASS    |
| o03-e03-build-available-exams-page             | Quizzes render as exam cards                                                                   | PASS    |
| o03-e03-build-available-exams-page             | Cards show title, count, Start Exam                                                            | PASS    |
| o03-e03-build-available-exams-page             | Start Exam transitions toward exam view                                                        | PASS    |
| o03-e03-build-available-exams-page             | Empty state when no quizzes                                                                    | PASS    |
| o03-e03-build-available-exams-page             | Question Bank / Quiz Builder unaffected                                                        | PASS    |
| o03-e04-build-exam-question-view               | Attempt created and first question loads                                                       | PASS    |
| o03-e04-build-exam-question-view               | Options highlighted on select                                                                  | PASS    |
| o03-e04-build-exam-question-view               | Save-answer API called on select                                                               | PASS    |
| o03-e04-build-exam-question-view               | Navigation restores answers                                                                    | PASS    |
| o03-e04-build-exam-question-view               | Progress indicator shown                                                                       | PASS    |
| o03-e04-build-exam-question-view               | Submit passes payload to results view                                                          | PASS    |
| o03-e04-build-exam-question-view               | Navigating away before submit is safe                                                          | PASS    |
| o03-e05-build-results-page                     | Score summary with percentage and counts                                                       | PASS    |
| o03-e05-build-results-page                     | Answer Review for every question                                                               | PASS    |
| o03-e05-build-results-page                     | Correct/incorrect styling distinct                                                             | PASS    |
| o03-e05-build-results-page                     | Retry Quiz restarts same quiz                                                                  | PASS    |
| o03-e05-build-results-page                     | Back to Exams returns to listing                                                               | PASS    |
| o03-e05-build-results-page                     | No extra API calls                                                                             | PASS    |
| o03-e06-add-tests-and-release-verification     | `py -m pytest tests/ -v` passes                                                                | PASS    |
| o03-e06-add-tests-and-release-verification     | Full exam flow with correct score                                                              | PASS    |
| o03-e06-add-tests-and-release-verification     | Abandoned attempt unscored                                                                     | PASS    |
| o03-e06-add-tests-and-release-verification     | Double submit returns 409                                                                      | PASS    |
| o03-e06-add-tests-and-release-verification     | Manual walkthrough documented                                                                  | PASS    |
| o03-e06-add-tests-and-release-verification     | V1/V2 regression unaffected                                                                    | PASS    |
