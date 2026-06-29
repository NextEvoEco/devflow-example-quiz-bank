# Intent: Quiz Bank - Quiz Builder

**ID:** i02-quiz-builder
**Date:** 2026-06-28
**Status:** draft
**Source:** user prompt

---

## 1. Original Request

> Extend the Quiz Bank application by allowing users to create reusable quizzes from the existing question bank.

Users should be able to compose quizzes by selecting questions, arranging their order, and managing quiz information without modifying the existing Question Bank functionality.

---

## 2. Motivation

After a reusable question bank has been established, the next step is to organize questions into quizzes.

This iteration introduces the ability to create and manage quizzes while keeping the Question Bank independent.

Separating question management from quiz management provides a clearer application structure and prepares the project for future online examination functionality.

---

## 3. Known Constraints

* The existing Question Bank module must remain unchanged.
* Quiz Builder should reuse questions from the Question Bank.
* Questions should not be duplicated.
* A quiz consists only of metadata and references to selected questions.
* The approved application layout and navigation should remain unchanged.
* Future online examination functionality is outside the scope of this iteration.
* Every development iteration should begin with a new Intent.

---

## 4. Unknowns

The following items require clarification before defining the Objective.

* Required quiz metadata
* Maximum number of questions per quiz
* Question ordering behavior
* Support for random question order
* Support for multiple quiz types
* Validation rules for incomplete quizzes
* Preview behavior
* Storage model for quiz-question relationships

---

## 5. Notes

This Intent preserves the user's original request without performing requirement analysis.

Requirement clarification should occur during the Interview phase.

Objective definition, task decomposition, implementation planning, and database design should not be included in this document.

This document represents the starting point of a single DevFlow development iteration.
