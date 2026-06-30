# Interview: Quiz Bank - Online Exam

**ID:** i03-online-exam
**Intent Ref:** `.devflow/intent/i03-online-exam.md`
**Date:** 2026-06-30
**Status:** confirmed

---

## 1. Goal Of This Interview

Remove ambiguity around the Online Exam flow before defining the V3 objective.

Key uncertainties: how exams are started, whether timing is required, how answers are persisted, what results are shown, and whether multiple modes are needed.

---

## 2. Questions

| #   | Question                                             | Reason                                | Status   |
| --- | ---------------------------------------------------- | ------------------------------------- | -------- |
| 1   | How does a user start an exam from an existing quiz? | Determines entry point and navigation | answered |
| 2   | Is the exam timed?                                   | Affects UI and backend requirements   | answered |
| 3   | Are answers submitted per question or all at once?   | Affects persistence strategy          | answered |
| 4   | Can users navigate freely between questions?         | Affects question UI layout            | answered |
| 5   | What is shown on the results page?                   | Determines result data model and UI   | answered |
| 6   | Should exam attempts be persisted to the database?   | Affects backend schema                | answered |
| 7   | Can users review correct answers after finishing?    | Affects result page design            | answered |
| 8   | What happens if the user abandons an exam mid-way?   | Affects attempt lifecycle             | answered |
| 9   | Is there a practice mode separate from exam mode?    | Affects scope and feature count       | answered |

---

## 3. Answers

| #   | Answer                                                                                                                           | Source        |
| --- | -------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| 1   | Dedicated Online Exam page with Available Exams list; each quiz card shows title, description, question count, Start Exam button | user + mockup |
| 2   | No timer                                                                                                                         | user          |
| 3   | Each answer is saved immediately when selected; no explicit per-question submit step                                             | user          |
| 4   | Free navigation — users can move forward and backward between questions at any time                                              | user          |
| 5   | Score percentage (dial), correct count, incorrect count, per-question Answer Review with user answer and correct answer          | user + mockup |
| 6   | Yes — exam attempts must be persisted to the database                                                                            | user          |
| 7   | Yes — correct answers are shown in the Answer Review section after submission                                                    | user          |
| 8   | Abandoned attempts are invalid and discarded; no resume mechanism needed                                                         | user          |
| 9   | One mode only: formal exam (answers revealed only after submission)                                                              | user          |

---

## 4. Clarified Constraints

- Online Exam entry point is a standalone page listed in the main navigation.
- Available Exams page shows all saved quizzes as exam cards (title, description, question count, Start Exam).
- No countdown timer in V3.
- Answer selections are persisted immediately (per-question auto-save); final submission is still a distinct user action.
- Question navigation is free — users may revisit any question before submitting.
- Results page shows: score percentage, correct count, incorrect count, and a per-question Answer Review with the user's answer and the correct answer highlighted.
- Exam attempts are stored in the database (quiz ref, answers, score, timestamp).
- Correct answers are revealed only on the results page after submission.
- Mid-exam abandonment discards the attempt; no partial-attempt recovery.
- Single exam mode only — no separate practice mode in V3.
- Existing Question Bank and Quiz Builder modules must remain unaffected.

---

## 5. Remaining Unknowns

None — all items from the intent have been resolved.

---

## 6. Interview Outcome

Planning can proceed.

All unknowns from the intent are resolved. The V3 objective can now be defined with full scope, data model, and UI specification.
