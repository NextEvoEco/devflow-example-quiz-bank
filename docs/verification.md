# Quiz Bank — Local Run & Verification Guide

This guide documents how to start the app locally, run its automated checks, and
manually verify the releaseable scope for V1 (Question Bank) and V2 (Quiz
Builder). For V3 (Online Exam), see [v3-verification.md](v3-verification.md).
It is written so a fresh user or AI session can reproduce verification without
prior context.

---

## 1. Prerequisites

- Python 3.13+
- `pip`

Install dependencies from the repository root:

```bash
pip install -r requirements.txt
```

---

## 2. Run The Automated Tests

```bash
py -m pytest
```

Expected result: all tests pass. The suite covers the V1 and V2 baselines:

| Test file                           | Covers                                                                 |
| ----------------------------------- | ---------------------------------------------------------------------- |
| `tests/test_bootstrap.py`           | app startup + automatic SQLite initialization                          |
| `tests/test_question_repository.py` | storage layer CRUD, search, validation, difficulty default             |
| `tests/test_questions_api.py`       | `/api/questions` success and error responses                           |
| `tests/test_question_bank_page.py`  | Question Bank page shell + API-driven list/search                      |
| `tests/test_question_flows.py`      | add / edit / delete UI surface + lifecycle                             |
| `tests/test_v1_release.py`          | V1 startup, persistence across restart, full lifecycle, scope boundary |
| `tests/test_quiz_schema.py`         | schema v2 migration (`quizzes`, `quiz_questions`)                      |
| `tests/test_quizzes_api.py`         | `/api/quizzes` CRUD, min-3 / existence / duplicate validation          |
| `tests/test_quiz_list_page.py`      | Quiz List page + navigation controller                                 |
| `tests/test_quiz_builder_page.py`   | Quiz Builder markup + create/edit lifecycle                            |
| `tests/test_quiz_preview.py`        | Quiz Preview modal + hook wiring                                       |
| `tests/test_o02_release.py`         | V2 full lifecycle, min-3 rule, QB regression, scope boundary           |

For the V3 (Online Exam) test files and manual steps, see
[v3-verification.md](v3-verification.md).

---

## 3. Start The Application

```bash
py -m backend
```

- Serves on `http://127.0.0.1:5000/` by default.
- Set the `PORT` environment variable to use a different port.
- The SQLite database is created automatically on first start at
  `data/quiz_bank.db`. The bank starts empty.

Open `http://127.0.0.1:5000/` in a browser.

---

## 4. Manual Verification Checklist

Perform these steps in the browser to confirm the V1 Question Bank:

1. **Empty state** — On a clean database, the page shows the "No questions yet"
   empty state and a count badge of `0`.
2. **Add** — Click **Add Question**, fill all fields, choose a correct answer
   and difficulty, and **Save**. The question appears in the list and the count
   increases.
3. **Validation** — Open **Add Question**, leave fields blank, and **Save**.
   Inline field errors and a form-level message appear; nothing is saved.
4. **Search** — Type in the search box. The list filters in real time
   (case-insensitive). A non-matching term shows the "No questions found"
   empty state.
5. **Edit** — Click **Edit** on a row. The editor opens pre-filled. Change a
   value and **Save**; the row updates.
6. **Delete** — Click **Del** on a row, confirm in the dialog. The row is
   removed. Cancelling (button, backdrop, or Escape) leaves it intact.
7. **Persistence** — Stop the server (`Ctrl+C`) and restart with
   `py -m backend`. Previously added questions are still listed.

---

## 4b. Manual Verification Checklist — Quiz Builder (V2)

From the sidebar, click **Quiz Builder**:

1. **Empty state** — With no quizzes, the page shows "No quizzes yet".
2. **Create** — Click **New Quiz**, enter a name, and **Add** 3+ questions from
   the Add Questions panel (each moves to Selected Questions).
3. **Reorder** — Use the ↑/↓ controls in the Selected panel to change order.
4. **Preview** — Click **Preview**. All selected questions appear in the current
   order, each showing options A–D with the correct answer marked. Close it.
5. **Min-3 rule** — Remove questions until only 2 remain and click **Save Quiz**.
   An error "A quiz requires at least 3 questions." is shown; nothing is saved.
6. **Save** — Add back to 3+ and **Save Quiz**. You return to the Quiz List and
   the quiz appears as a card with its question count.
7. **Edit** — Click **Edit** on a card. Name and question order are pre-filled.
   Rename, add/remove/reorder, and **Save Quiz**; the card updates.
8. **Delete** — Click **Delete** on a card and confirm. The card is removed.

---

## 5. Scope Confirmation (V1 + V2 + V3)

The app implements all three planned versions: Question Bank (V1), Quiz Builder
(V2), and Online Exam (V3). See [v3-verification.md](v3-verification.md) for the
V3 checklist. Out of scope across all versions:

- Authentication, multi-user isolation, or cloud deployment.
- Practice mode, exam timers, or attempt-history listing (V3).

Deleting a question that a quiz references removes it from that quiz automatically
(SQLite cascade), so the Question Bank remains fully independent of Quiz Builder
and Online Exam.
