# Evidence: Quiz Preview

**ID:** o02-e05-quiz-preview
**Task Ref:** `.devflow/tasks/o02/t05-quiz-preview.md`
**Executed By:** Claude Code
**Execution Date:** 2026-07-07
**Execution Time:** ~35 min
**Status:** completed

---

## 1. Summary

Implemented the Quiz Preview as a modal overlay, fulfilling the
`window.openQuizPreview(draft)` hook that the t04 builder's Preview button
already calls. The modal shows every question in the user-defined order, each
with its text, all four options A–D, and a clearly marked correct answer (green
highlight + "✓ Correct"). It renders from the builder's in-memory draft, so it
reflects unsaved changes (including reordering) without requiring a save, and it
can equally render a saved quiz since `GET /api/quizzes/<id>` returns the same
`questions` shape. No backend or API changes were needed. Verified with 91
passing tests and a real-browser session covering open, order, correct-answer
marking, unsaved-reorder reflection, and dismissal.

---

## 2. Files Changed

| File                          | Change Type | Description                                                                                                                                       |
| ----------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/index.html`         | modified    | Added the Quiz Preview modal overlay; loads `quiz-preview.js`                                                                                     |
| `frontend/js/quiz-preview.js` | created     | Defines `window.openQuizPreview(draft)`; renders ordered questions with options A–D and correct-answer marking; close via ×/Close/backdrop/Escape |
| `frontend/css/style.css`      | modified    | Preview modal (600px), question cards, option rows, correct-answer highlight                                                                      |
| `tests/test_quiz_preview.py`  | created     | 4 tests: modal markup, JS hook + wiring, builder-calls-hook, saved-quiz shape matches draft                                                       |

---

## 3. Behavior Added

* The builder's Preview button opens a modal titled `Preview: <quiz name>`.
* Each question renders as a card: "Question N" label, question text, and a list
  of four options (A–D); the correct option is highlighted and labelled "✓ Correct".
* Questions appear in the current builder order, including unsaved reordering.
* The modal is dismissible via the × button, the Close button, a backdrop click,
  or the Escape key, returning the user to the builder.
* Empty draft renders a "No questions to preview." message (defensive).

---

## 4. Test Results

### Acceptance Criteria Verification

| Criterion                                                                      | Result | Notes                                                           |
| ------------------------------------------------------------------------------ | ------ | --------------------------------------------------------------- |
| Clicking "Preview" in the Quiz Builder opens the preview                       | PASS   | Preview button → modal opened, title "Preview: My Preview Quiz" |
| All selected questions are shown in order                                      | PASS   | 3 questions in builder order                                    |
| Each question displays text, options A–D, and the correct answer               | PASS   | 4 options each; correct = A/B/C highlighted per seed data       |
| Preview reflects the current in-builder question order (incl. unsaved changes) | PASS   | reordered in builder → reopened → preview order matched exactly |
| User can close/dismiss the preview and return to the builder                   | PASS   | Close button, Escape, and backdrop click all dismiss            |

### Test Output

```
$ python -m pytest -q
91 passed in 1.81s

# Live browser verification (4 questions seeded, correct answers A/B/C/D):
- builder: add 3, name "My Preview Quiz", click Preview
  -> modal open; 3 questions in order; each 4 options; correct marks A, B, C
- close, reorder (move "Boiling point" to top), reopen
  -> preview order == builder order (unsaved change reflected)
- Escape -> dismissed; reopen -> backdrop click -> dismissed
- console errors: none
```

Screenshot captured showing the highlighted correct answers and "✓ Correct" markers.

---

## 5. Known Limitations

* Preview always shows the correct answer (by design — this is a builder review,
  not the exam runtime, which is V3).
* No print/export/share (out of scope).

---

## 6. Next Suggested Task

**Next task:** `o02/t06-integration-testing` (final V2 task)
**Context:** All V2 Quiz Builder functionality is implemented: schema, `/api/quizzes`
CRUD with min-3 validation, quiz list page, builder (create/edit/reorder), and
preview. 91 tests pass. t06 should add integration/release verification for V2 —
the full create→list→edit→preview→delete flow, the min-3 rule, no-regression on
the Question Bank, and confirmation that Online Exam (V3) remains out of scope.
The app runs via `py -m backend`; tests via `py -m pytest`. Frontend page/nav
structure is documented in `.devflow/memory.md`.
