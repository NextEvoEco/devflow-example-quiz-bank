# Interview: Quiz Bank - Question Bank

**ID:** i01-question-bank
**Intent Ref:** `.devflow/intent/i01-question-bank.md`
**Date:** 2026-06-28
**Status:** confirmed

---

## 1. Goal Of This Interview

> What uncertainty is this interview trying to remove?

This interview clarifies the first implementation boundary for the Quiz Bank example project so that a concrete objective can be defined without guessing stack, scope, or validation expectations.

---

## 2. Questions

| #   | Question                                                                                                                                                                                                                    | Reason                                                                                                                   | Status   |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------- |
| 1   | For the first objective, do you want to build only a front-end single-page demo, or should the example include any backend or persistence layer?                                                                            | This determines the architecture boundary and stack selection.                                                           | answered |
| 2   | For the first objective, which user flows must be completed end-to-end: Question Bank only, Question Bank + Quiz Builder, or all the way through Online Exam?                                                               | This defines scope and keeps the first objective bounded.                                                                | answered |
| 3   | What level of implementation quality do you want for the first objective: UI prototype only, working functional example with in-memory state, or a more production-like baseline with tests and validation?                 | This sets success criteria, testing scope, and delivery expectations.                                                    | answered |
| 4   | For "include everything" in architecture, do you want the first objective to include a real backend API and persistence, or is a self-contained front-end app with local/in-memory data acceptable for the first milestone? | Q1 indicates broad architecture scope, but this needs a concrete implementation boundary for Objective 1.                | answered |
| 5   | What front-end stack do you want for the example: plain HTML/CSS/JavaScript, React, Vue, or another choice?                                                                                                                 | The UI spec exists, but the implementation stack is still undefined.                                                     | answered |
| 6   | What data persistence level do you want for the first objective: memory only, browser localStorage, or a real database?                                                                                                     | This affects whether the app can be independently demonstrated across refreshes and how much infrastructure is required. | answered |
| 7   | For a releaseable V1 using plain HTML/CSS/JavaScript with SQLite, what backend technology do you want: Node.js, Python, or another option?                                                                                  | SQLite implies a runtime layer outside the browser, so the backend stack must be explicit.                               | answered |
| 8   | For V1 Question Bank, should the functional scope be limited to add, edit, delete, list, and search questions only, with no quiz-building or exam-taking features yet?                                                      | This locks the first release boundary.                                                                                   | answered |
| 9   | What is the minimum release-quality bar for V1: manual demo only, or do you also want automated checks such as basic tests and validation?                                                                                  | "Releaseable" needs a concrete success definition.                                                                       | answered |
| 10  | For V1, do you want the app delivered as a simple local web app started by a Python server, or as a desktop-like local-only app structure?                                                                                  | This defines the runtime and delivery model for a releaseable local demo.                                                | answered |
| 11  | Should V1 preload any sample questions so the app is usable immediately after startup, or should it begin with an empty question bank?                                                                                      | This affects first-run usability and acceptance criteria.                                                                | answered |
| 12  | For question validation, what minimum fields must be required in V1: question text, options A-D, correct answer, and difficulty?                                                                                            | This confirms the validation contract for add/edit flows.                                                                | answered |

---

## 3. Answers

| #   | Answer                                                                                                                | Source |
| --- | --------------------------------------------------------------------------------------------------------------------- | ------ |
| 1   | Include the full architecture scope rather than limiting to front-end only.                                           | user   |
| 2   | The first objective should focus on Question Bank only.                                                               | user   |
| 3   | It should be independently executable, demonstrable, and usable.                                                      | user   |
| 4   | V1 to V3 should differ mainly by feature scope expansion, and every version should still be releaseable.              | user   |
| 5   | Use plain HTML/CSS/JavaScript.                                                                                        | user   |
| 6   | Use SQLite.                                                                                                           | user   |
| 7   | Use Python.                                                                                                           | user   |
| 8   | Yes. V1 should be limited to list, search, add, edit, and delete questions only, without quiz builder or online exam. | user   |
| 9   | V1 should include basic validation, error handling, and basic automated tests.                                        | user   |
| 10  | Deliver it as a normal local web app started by a Python server.                                                      | user   |
| 11  | Do not preload sample questions. Start from an empty question bank.                                                   | user   |
| 12  | Require question text, options A-D, and correct answer. Difficulty should have a default value.                       | user   |

---

## 4. Clarified Constraints

- This is a demonstration project, not a commercial product.
- The implementation should remain intentionally lightweight.
- The application should use the approved UI design.
- The project should follow the DevFlow workflow.
- The first objective scope is limited to Question Bank.
- The first objective should result in something independently executable and usable.
- V1 to V3 should mainly expand by feature scope, while each version remains releaseable.
- The front-end stack is plain HTML/CSS/JavaScript.
- The data layer should use SQLite.
- The backend stack is Python.
- V1 scope is limited to Question Bank CRUD and search.
- V1 must include basic validation, error handling, and basic automated tests.
- V1 should be delivered as a normal local web app.
- V1 should start with an empty question bank.
- Question text, options A-D, and correct answer are required fields.
- Difficulty should have a default value rather than being required input on first render.

---

## 5. Remaining Unknowns

- None at this stage.

---

## 6. Interview Outcome

> Can planning proceed?

Yes. The information is sufficient to draft and confirm the first objective.
