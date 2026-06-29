# Interview: Quiz Builder

**ID:** i02-quiz-builder
**Intent Ref:** `.devflow/intent/i02-quiz-builder.md`
**Date:** 2026-06-28
**Status:** confirmed

---

## 1. Goal Of This Interview

Remove uncertainty around quiz metadata, question limits, ordering behavior, validation rules, and preview requirements before defining the Quiz Builder objective.

---

## 2. Questions

| #   | Question                                                               | Reason                                                                  | Status   |
| --- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------- | -------- |
| 1   | What metadata fields does a Quiz require?                              | Determines the quiz creation form and data model                        | answered |
| 2   | Is there a maximum number of questions per quiz?                       | Determines whether a cap needs to be enforced in validation             | answered |
| 3   | Can users manually reorder questions inside a quiz?                    | Determines whether ordering UI and position persistence are required    | answered |
| 4   | Should the quiz support a random question order setting?               | Determines whether a shuffle flag needs to be stored and surfaced in UI | answered |
| 5   | What is the minimum number of questions required to save a valid quiz? | Determines the validation rule for quiz completeness                    | answered |
| 6   | Should users be able to preview the full quiz content in Quiz Builder? | Determines whether a preview view is required in this iteration         | answered |

---

## 3. Answers

| #   | Answer                                                                 | Source |
| --- | ---------------------------------------------------------------------- | ------ |
| 1   | Name only. No description, difficulty tag, or other metadata required. | user   |
| 2   | No maximum limit.                                                      | user   |
| 3   | Yes. Users can manually reorder questions inside a quiz.               | user   |
| 4   | No random order. Question order is fixed as arranged by the user.      | user   |
| 5   | Minimum 3 questions required to save a quiz.                           | user   |
| 6   | Yes. A preview of the full quiz content is required in Quiz Builder.   | user   |

---

## 4. Clarified Constraints

- Quiz metadata is limited to name only
- No maximum question count per quiz
- Users can manually reorder questions within a quiz
- Question order is fixed; no shuffle setting is required
- A quiz requires at least 3 questions to be valid and saveable
- Quiz Builder must include a preview view of the full quiz
- The existing Question Bank module must remain unchanged
- Questions are referenced, not duplicated
- Future Online Exam functionality is out of scope for this iteration

---

## 5. Remaining Unknowns

- Storage model for quiz-question relationships (to be decided during planning)
- Whether multiple quiz types are needed (not raised; assumed out of scope for this iteration)

---

## 6. Interview Outcome

All user-facing uncertainties are resolved. Planning can proceed.

The objective should cover: quiz creation with name, question selection from the existing bank, manual reordering, a minimum-3-question validation rule, and a preview view. The Question Bank must remain independent and unchanged.
