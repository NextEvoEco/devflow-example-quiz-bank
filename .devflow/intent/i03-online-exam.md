# Intent: Quiz Bank - Online Exam

**ID:** i03-online-exam
**Date:** 2026-06-29
**Status:** draft
**Source:** user prompt

---

## 1. Original Request

> Extend the Quiz Bank application with an Online Exam flow based on saved quizzes.

Users should be able to take an exam using quizzes created in Quiz Builder, submit answers, and view exam-related results without breaking existing Question Bank or Quiz Builder behavior.

---

## 2. Motivation

The Question Bank and Quiz Builder iterations established reusable questions and reusable quizzes.

The next step is to let those quizzes be used in an actual exam-taking flow.

This iteration introduces the learner-facing runtime experience that turns stored quiz content into a usable online exam while preserving the existing content-management modules.

---

## 3. Known Constraints

* The existing Question Bank module must remain functional.
* The existing Quiz Builder module must remain functional.
* Online Exam should reuse saved quizzes rather than duplicating question content.
* The approved application layout and navigation should remain unchanged unless the new flow requires clearly scoped additions.
* This Intent should capture the request only; detailed planning belongs to later artifacts.
* Every development iteration should begin with a new Intent.

---

## 4. Unknowns

The following items require clarification before defining the Objective.

* How users start an exam from an existing quiz
* Whether an exam attempt should be timed
* Whether answers are submitted once at the end or per question
* Whether users can move backward and forward between questions
* What results should be shown after submission
* Whether exam attempts should be persisted
* Whether users can review correct answers after finishing
* Validation rules for incomplete or abandoned attempts
* Any differences between practice mode and exam mode

---

## 5. Notes

This Intent preserves the user's request without performing requirement analysis.

Requirement clarification should occur during the Interview phase.

Objective definition, task decomposition, implementation planning, storage design, and UI details should not be included in this document.

This document represents the starting point of a new DevFlow development iteration for V3.
