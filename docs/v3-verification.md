# Quiz Bank V3 (Online Exam) — Verification Guide

This guide documents how to verify the Online Exam (V3) module. It complements
[verification.md](verification.md), which covers V1 (Question Bank) and V2
(Quiz Builder). It is written so a fresh user or AI session can reproduce
verification without prior context.

---

## 1. Run The Automated Tests

```bash
py -m pytest
```

Expected: all tests pass. V3-specific coverage:

| Test file                         | Covers                                                                            |
| --------------------------------- | --------------------------------------------------------------------------------- |
| `tests/test_exam_repository.py`   | schema v3 (`exam_attempts`, `exam_answers`) + repository CRUD                     |
| `tests/test_exam_api.py`          | `/api/exams` create / save-answer / submit + error cases                          |
| `tests/test_exam_list_page.py`    | Available Exams page + Online Exam nav                                            |
| `tests/test_exam_taking_page.py`  | in-exam view markup + wiring + full API flow                                      |
| `tests/test_exam_results_page.py` | results page markup + wiring + submit payload                                     |
| `tests/test_v3_release.py`        | full flow, scoring, abandonment, double-submit, no correct-leak, V1/V2 regression |

---

## 2. Start The Application

```bash
py -m backend
```

Open `http://127.0.0.1:5000/` and click **Online Exam** in the sidebar.

> When seeding data while the dev server is running, seed **through the app's own
> API** (e.g. POST to `/api/questions` and `/api/quizzes`). Running a separate
> Python process that opens `data/quiz_bank.db` while the reloader dev server
> holds it can cause transient `no such table` errors.

You need at least one saved quiz (create one in **Quiz Builder** first).

---

## 3. Manual Verification Checklist — Online Exam (V3)

1. **Available Exams** — Online Exam shows a card per saved quiz (name +
   question count + **Start Exam**). With no quizzes, an empty state appears.
2. **Start Exam** — Click **Start Exam**. The first question loads with four
   labeled options (A–D), a progress bar, question-number buttons, and Previous
   (dimmed on Q1) / Next.
3. **Answer** — Click an option. It highlights (single-select, checkmark) and is
   saved immediately. The correct answer is **not** revealed.
4. **Navigate** — Use Next/Previous and the question-number buttons to move
   freely. Returning to a question restores your saved selection.
5. **Submit** — On the last question the button reads **Submit**. Submitting an
   exam (answering all, some, or none) shows the Results page.
6. **Results** — Verify the quiz name, "Exam Complete!", the score ring
   (green ≥70% / amber 50–69% / red <50%) with percentage and score/total, and
   the Correct/Incorrect count cells. The Answer Review lists every question with
   your answer, the correct answer (shown only when you were wrong), and a
   Correct/Incorrect indicator. Unanswered questions show "Not answered".
7. **Retry Quiz** — Starts a fresh attempt on the same quiz (Q1, no selections).
8. **Back to Exams** — Returns to the Available Exams listing.
9. **Abandon** — Start an exam, then navigate to another section before
   submitting. No error occurs; the attempt is left unscored in the database.
10. **No regression** — Question Bank (list/search/add/edit/delete) and Quiz
    Builder (list/create/edit/preview/delete) still work.

---

## 4. Scope Confirmation (V3)

The application now delivers all three planned versions:

- V1 — Question Bank
- V2 — Quiz Builder
- V3 — Online Exam

V3 is a single formal exam mode: correct answers are revealed only on the results
page after submission. There is no practice mode, no timer, and no attempt-history
listing (out of scope). Abandoned attempts are not scored. Existing Question Bank
and Quiz Builder behavior is unchanged; these boundaries are guarded by
`tests/test_v3_release.py`.
