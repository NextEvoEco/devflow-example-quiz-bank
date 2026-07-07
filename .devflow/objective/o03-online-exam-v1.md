# Objective: Online Exam V1

**ID:** o03-online-exam-v1
**Version:** V3
**Date:** 2026-06-30
**Status:** draft
**Interview Ref:** `.devflow/interview/i03-online-exam.md`

---

## 1. Goal

> What problem does this version solve?
> Why is this the right thing to build now?

This version delivers the Online Exam flow, allowing users to take exams based on quizzes created in the Quiz Builder, submit answers, and view a detailed results page.

It is the right thing to build now because Question Bank (V1) and Quiz Builder (V2) have established reusable content. The next natural step is to make that content consumable through an exam-taking runtime, completing the core application loop.

---

## 2. Background

Quiz Bank is the official DevFlow example project. V1 delivered question management. V2 delivered quiz composition. V3 closes the loop by delivering the learner-facing exam experience.

The approved UI specification already defines the Online Exam flow including an Available Exams listing page, an in-exam question view with free navigation, and a results page with score summary and per-question Answer Review.

This objective implements that flow while keeping all existing Question Bank and Quiz Builder modules fully intact.

---

## 3. Scope

### In Scope

* Online Exam navigation entry in the main sidebar.
* Available Exams page listing all saved quizzes as exam cards (title, description, question count, Start Exam button).
* In-exam question view with free forward/backward navigation between questions.
* Answer selection saved immediately per question (no explicit per-question submit step).
* Final Submit button that ends the exam and triggers scoring.
* Abandoned attempts (browser close / nav away before submit) are discarded and not persisted.
* Results page showing: score percentage dial, correct count, incorrect count, per-question Answer Review with user answer and correct answer.
* Exam attempts persisted to the database (quiz reference, per-question answers, score, timestamp).
* Single formal exam mode — correct answers revealed only on the results page after submission.
* Retry Quiz action on the results page to start a new attempt on the same quiz.
* Back to Exams action on the results page to return to the Available Exams listing.

### Out of Scope

* Practice mode or any mode other than formal exam.
* Countdown timer or time-limited exams.
* Exam attempt history listing or per-user attempt tracking.
* Authentication or multi-user isolation.
* Modifying or extending Question Bank or Quiz Builder behavior.
* Cloud deployment or production hardening beyond V3 baseline.

---

## 4. Constraints

| Type       | Constraint                                                                                      |
| ---------- | ----------------------------------------------------------------------------------------------- |
| Platform   | Local web application, same runtime as V1 and V2                                                |
| Tech Stack | Python backend, plain HTML/CSS/JavaScript frontend, SQLite database                             |
| Trigger    | Manual local startup by the user                                                                |
| Output     | A releaseable V3 Online Exam module integrated into the existing Quiz Bank application          |
| Other      | Must not break existing Question Bank or Quiz Builder modules; follow approved UI specification |

---

## 5. Success Criteria

> How will we know this objective is complete?

* [ ] Available Exams page lists all saved quizzes and allows starting an exam from any quiz.
* [ ] In-exam view displays one question at a time with free navigation between all questions in the quiz.
* [ ] Answer selections are saved immediately; the user can change answers before submitting.
* [ ] Submitting an exam records the attempt (quiz ref, answers, score, timestamp) in the database.
* [ ] Results page displays score percentage, correct count, incorrect count, and per-question Answer Review with correct answers highlighted.
* [ ] Retry Quiz starts a fresh attempt; Back to Exams returns to the listing page.
* [ ] Abandoning an exam (navigating away before submit) does not persist a partial attempt.
* [ ] Existing Question Bank and Quiz Builder flows remain fully functional.
* [ ] Basic automated tests cover the exam flow and results logic.

---

## 6. Open Questions

> Unresolved issues at the time of writing. Must be resolved before task splitting begins.

| #   | Question | Owner | Status   |
| --- | -------- | ----- | -------- |
| 1   | None.    | —     | resolved |

---

## 7. Confirmation

**Confirmed by:** {user}
**Confirmed at:** {YYYY-MM-DD HH:MM}

> Signature: {pending user confirmation}
