# 04 — User Guide

How to use Quiz Bank in the browser after the app is running at
`http://127.0.0.1:5000`.

There is no login. All data is stored in the local PostgreSQL database.

---

## Layout

The app is a single-page application with a fixed shell:

| Area        | Behavior                                                    |
| ----------- | ----------------------------------------------------------- |
| **Sidebar** | Switch between Question Bank, Quiz Builder, and Online Exam |
| **Top bar** | Shows the current section title                             |
| **Content** | The active page for that section                            |

Navigation uses in-page state (no URL routes). Clicking a sidebar item always opens
that section’s list view.

---

## 1. Question Bank

Manage multiple-choice questions (options A–D, one correct answer, difficulty).

### Browse and search

1. Open **Question Bank** in the sidebar.
2. The table lists question text, difficulty badge, and actions.
3. Type in **Search questions...** to filter by question text (case-insensitive).
4. If nothing matches, an empty state is shown.

### Add a question

1. Click **Add Question**.
2. Fill in:
   - Question text (required)
   - Options A–D (required)
   - Correct Answer: A, B, C, or D
   - Difficulty: Easy, Medium, or Hard (defaults to Medium if omitted on the API)
3. Click **Save Question**.
4. The new row appears in the list.

### Edit a question

1. Click **Edit** on a row.
2. Change fields in the modal.
3. Click **Save Question**.

### Delete a question

1. Click **Del** on a row.
2. Confirm in the dialog.
3. The question is removed from the bank. If it was used in quizzes, its join rows
   are removed as well (cascade).

---

## 2. Quiz Builder

Assemble named quizzes from existing questions. A quiz needs **at least three**
questions.

### Quiz list

1. Open **Quiz Builder** in the sidebar.
2. Each card shows the quiz name and question count.
3. Actions:
   - **New Quiz** — create
   - **Edit** — open the builder for that quiz
   - **Delete** — confirm and remove the quiz (questions in the bank are kept)

### Create or edit a quiz

1. Enter a **quiz name** (required).
2. In **Add Questions**, click **Add** to move bank questions into the quiz.
3. In **Selected Questions**:
   - Remove a question with **×**
   - Reorder with up/down controls (order is saved as `position`)
4. Optionally open **Preview** to review full text, options, and correct answers
   before saving (preview works on the in-memory selection).
5. Click **Save Quiz**.
   - Fewer than three selected questions → save is blocked with an error message.
6. **Cancel** / back returns to the quiz list.

---

## 3. Online Exam

Take any saved quiz as an exam and review scored results.

### Available exams

1. Open **Online Exam** in the sidebar.
2. Each card is a saved quiz.
3. Click **Start Exam** to begin.

### Taking an exam

1. One question is shown at a time with options A–D.
2. Select an answer — it is saved immediately to the server.
3. Use navigation controls to move between questions (answers are kept).
4. Click **Submit** when finished.
5. Click **Exit** to leave without submitting (the attempt stays unscored).

Correct answers are **not** shown until after submit.

### Results

After submit you see:

- Score (correct / total) and percentage
- Answer review: your choice vs the correct option per question

Actions:

- **Back to Exams** — return to the exam list
- **Retry Quiz** — start a new attempt for the same quiz

---

## Typical workflows

### Build a small bank and a quiz

1. Question Bank → add at least three questions.
2. Quiz Builder → New Quiz → select those questions in order → Save.
3. Online Exam → Start Exam → answer → Submit → review results.

### Use the demo seed

If you imported the demo dataset (`scripts/import_seed_from_sqlite.py`):

1. Question Bank shows ~50 geography questions.
2. Quiz Builder lists three ready-made quizzes.
3. Online Exam can start any of those quizzes immediately.

---

## Tips and limits

- Refreshing the browser reloads data from the API; unfinished exam UI state is not
  restored from the server as an “in progress” session UI.
- There is no multi-user auth; anyone with access to the local URL can change data.
- Difficulty colors: Easy (green), Medium (amber), Hard (red).

---

## Related docs

- [03-deployment.md](03-deployment.md) — how to start the app
- [05-api-reference.md](05-api-reference.md) — HTTP endpoints used by the UI
