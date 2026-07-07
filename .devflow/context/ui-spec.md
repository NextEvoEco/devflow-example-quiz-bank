# Quiz Bank — UI Context Document

> **Purpose:** This document describes the application structure, page behaviours, component contracts, and data model for the Quiz Bank web application. It is intended as the primary UI context for AI-assisted development. Implement behaviour as described; do not infer from visual presentation alone.

> **Status:** This file is the final target UI/product specification and may intentionally be ahead of the current repository implementation.

> **Implementation Note:** The current repository may implement only a subset of this document. When working on the live codebase, always pair this file with `.devflow/context/architecture.md`, `.devflow/context/stack.md`, and `.devflow/status.md` to distinguish target scope from currently shipped scope.

---

## Application Overview

Quiz Bank is a lightweight, single-page educational application. It allows users to:

1. Maintain a collection of multiple-choice questions (**Question Bank**).
2. Assemble questions into named quizzes (**Quiz Builder**).
3. Take those quizzes online and review their results (**Online Exam**).

The application runs entirely client-side with in-memory state. There is no backend, authentication, or persistent storage requirement in the current scope.

The interface is a single HTML page. All navigation is in-page state switching — no URL routing, no full-page reloads. All six views share one persistent layout shell (sidebar + top bar).

For avoidance of doubt:

- this section describes the target UI/product behavior
- the active repository implementation may temporarily ship only part of this scope
- context files may lead implementation, but should not fall behind the intended product direction

---

## Navigation Structure

### Layout Shell

The shell is always visible and consists of two fixed regions:

| Region      | Description                                                           |
| ----------- | --------------------------------------------------------------------- |
| **Sidebar** | Fixed left panel. Contains the app logo and three navigation items.   |
| **Top Bar** | Fixed header above the content area. Displays the current page title. |

Navigation is mutual-exclusive: exactly one page view is visible at a time inside the content area.

### Sidebar Navigation Items

| Label         | Navigates To     | Active When                                                 |
| ------------- | ---------------- | ----------------------------------------------------------- |
| Question Bank | `questions` page | `currentPage === 'questions'`                               |
| Quiz Builder  | `quizList` page  | `currentPage` is `quizList` or `quizCreate`                 |
| Online Exam   | `examList` page  | `currentPage` is `examList`, `examTaking`, or `examResults` |

The active item has a distinct background and text colour. Clicking a sidebar item always navigates to the list view for that section, never to a sub-view.

### Page IDs

The application tracks a single `currentPage` string. Valid values:

- `questions` — Question Bank list
- `quizList` — Quiz list
- `quizCreate` — Quiz create / edit form
- `examList` — Available exams list
- `examTaking` — Active exam session
- `examResults` — Exam results

---

## Pages

---

### 1. Question Bank (`questions`)

**Purpose:** View, search, add, edit, and delete questions.

**Layout:**
- Page header row: title ("Questions") + total count badge + "Add Question" primary button.
- Search box below the header, left-aligned, max width ~360 px.
- Question table fills the remaining width.
- If no questions match the search: empty state replaces the table.

**Main Components:**
- **Search box** — filters the question list in real time by question text (case-insensitive substring match).
- **Question table** — columns: Question text | Difficulty badge | Actions (Edit, Del).
- **Difficulty badge** — pill-shaped label; colour-coded: Easy = green, Medium = amber, Hard = red.
- **Empty state** — shown when the filtered list is empty. Contains an icon, a short message, and an "Add Question" button.

**User Actions:**
- Type in the search box → filters the table instantly; no submit required.
- Click **Add Question** (header or empty state) → opens the Question Editor modal in "Add" mode.
- Click **Edit** on a row → opens the Question Editor modal pre-filled with that question's data.
- Click **Del** on a row → opens the Delete Question confirmation dialog.

**Navigation Flow:**
- No navigation away from this page (all actions are modal/in-place).

---

### 2. Quiz List (`quizList`)

**Purpose:** View all created quizzes and initiate create / edit / delete operations.

**Layout:**
- Page header row: title ("Quizzes") + "New Quiz" primary button.
- Two-column card grid below the header.
- If no quizzes exist: empty state replaces the grid.

**Main Components:**
- **Quiz card** — displays quiz name, description, question count badge, and two action buttons (Edit, Delete).
- **Empty state** — shown when the quizzes list is empty. Contains an icon, message, and "Create Quiz" button.

**User Actions:**
- Click **New Quiz** → navigates to `quizCreate` in "New" mode (blank form).
- Click **Edit** on a card → navigates to `quizCreate` with that quiz's data pre-loaded.
- Click **Delete** on a card → opens the Delete Quiz confirmation dialog.

**Navigation Flow:**
- **New Quiz / Edit** → `quizCreate`
- **Sidebar** → any top-level section

---

### 3. Quiz Create / Edit (`quizCreate`)

**Purpose:** Create a new quiz or edit an existing one by naming it and selecting questions from the bank.

**Layout:**
- Back link ("← Back to Quizzes") above the page title.
- Page title: "New Quiz" or "Edit Quiz" depending on mode.
- Quiz details card (name + description inputs).
- "Selected Questions" panel — lists questions currently in the quiz.
- "Add Questions" panel — lists questions not yet in the quiz, with a search box.
- Footer action row: Cancel + Save Quiz buttons, right-aligned.
- Maximum content width: 720 px.

**Main Components:**
- **Quiz name input** — required text field.
- **Description textarea** — optional, 2 rows, non-resizable.
- **Selected Questions panel** — header with count badge; rows showing question text, difficulty badge, and a remove (×) button per row. Shows "No questions selected" message when empty.
- **Add Questions panel** — inline search box; rows showing question text, difficulty badge, and "Add" button. Shows "All questions added or no matches found" when empty. Only questions not already selected are shown.
- **Save Quiz button** — disabled-equivalent (no-op) if quiz name is empty.

**User Actions:**
- Edit quiz name or description → updates form state.
- Type in Add Questions search → filters available questions in real time.
- Click **Add** on an available question → moves it to Selected Questions.
- Click **×** on a selected question → removes it from Selected Questions (returns to available pool).
- Click **Save Quiz** → saves (create or update) and navigates to `quizList`.
- Click **Cancel** or **Back to Quizzes** → navigates to `quizList` without saving.

**Navigation Flow:**
- **Save / Cancel / Back** → `quizList`

---

### 4. Exam List (`examList`)

**Purpose:** Show available quizzes that the user can take as an exam.

**Layout:**
- Page title ("Available Exams").
- Two-column card grid of quiz cards.
- If no quizzes exist: empty state with message directing user to Quiz Builder.

**Main Components:**
- **Exam card** — displays quiz name, description, question count badge, and a full-width "Start Exam" primary button.
- **Empty state** — shown when no quizzes have been created yet.

**User Actions:**
- Click **Start Exam** → resets exam state (question index = 0, answers = {}) and navigates to `examTaking` for that quiz.

**Navigation Flow:**
- **Start Exam** → `examTaking`

---

### 5. Exam Taking (`examTaking`)

**Purpose:** Present one question at a time and collect the user's answers.

**Layout:**
- Centred column, max width 600 px.
- Header row: quiz name (small label) + current question counter ("Question N of M") on the left; "Exit" button on the right.
- Progress bar below the header — fills proportionally to (currentQuestion + 1) / total.
- Question card: question text + four answer option buttons (A, B, C, D).
- Navigation footer: "Previous" button (left) + "Next" or "Submit" button (right).

**Main Components:**
- **Progress bar** — visual only; no percentage label. Width updates with smooth transition on question change.
- **Question card** — white card with question text at top, then four option buttons stacked vertically.
- **Option button** — each displays a lettered label (A/B/C/D) and option text. When selected: label background becomes primary colour, border becomes primary colour, checkmark icon appears. Only one option can be selected per question.
- **Previous button** — visually dimmed (opacity 0.3) when on the first question; clicking has no effect when dimmed.
- **Next / Submit button** — labelled "Next" on all questions except the last; labelled "Submit" on the last question.

**User Actions:**
- Click an option → selects it for the current question (replaces any prior selection for that question).
- Click **Previous** → navigates to the previous question (no effect on question 1).
- Click **Next** → navigates to the next question.
- Click **Submit** (last question only) → ends the exam and navigates to `examResults`.
- Click **Exit** → navigates to `examList` without saving results.

**State Rules:**
- Previously selected answers are remembered when navigating back.
- An unanswered question is allowed (user can submit without answering all).

**Navigation Flow:**
- **Submit** → `examResults`
- **Exit** → `examList`

---

### 6. Exam Results (`examResults`)

**Purpose:** Display the exam outcome and allow the user to review each answer.

**Layout:**
- Centred column, max width 620 px.
- Title area: quiz name (small label above) + "Exam Complete!" heading.
- Score summary card: circular score indicator on the left; correct/incorrect counts on the right (two side-by-side cells).
- Answer Review panel: list of all questions with their result.
- Footer action row: "Back to Exams" + "Retry Quiz" buttons, centred.

**Main Components:**
- **Circular score indicator** — SVG ring showing score percentage. Colour: green ≥ 70 %, amber 50–69 %, red < 50 %. Centre displays percentage and "score / total" fraction.
- **Correct count cell** — green background, shows number of correct answers.
- **Incorrect count cell** — red background, shows number of incorrect answers.
- **Answer Review list** — one row per question:
  - Status icon (✓ or ✗) in a coloured circle.
  - Question text.
  - "Your answer: X: [text]" — shown for all questions.
  - "· Correct: X: [text]" — shown only when the user's answer was wrong.
  - Status badge: "Correct" or "Incorrect".

**User Actions:**
- Click **Back to Exams** → navigates to `examList`.
- Click **Retry Quiz** → resets exam state and navigates to `examTaking` for the same quiz.

**Navigation Flow:**
- **Back to Exams** → `examList`
- **Retry Quiz** → `examTaking` (same quiz, fresh state)

---

## Reusable Components

---

### Sidebar

**Behaviour:**
- Fixed width (220 px), full viewport height, does not scroll.
- Contains: app logo + name at top; nav items in the middle; no bottom section.
- Nav items are buttons (not anchor tags). Clicking always triggers in-page state change.
- Active item: visually highlighted (distinct background and text colour).
- Inactive items: hover state shows a subtle background change.

---

### Top Bar

**Behaviour:**
- Fixed height (56 px), spans the full content area width.
- Left side: page title text. Updates whenever `currentPage` changes.
- Right side: empty in this version (user account removed).
- Does not scroll.

---

### Question Table

**Structure:**
- Header row with column labels: Question | Difficulty | Actions.
- Data rows, one per question.
- Each row: full question text (wraps if long) | Difficulty badge | Edit + Del buttons.
- Rows have a subtle hover background.
- No built-in pagination — all filtered results are shown.

**Empty State:**
- Shown in place of the table when the filtered question list is empty.
- Contains: icon, "No questions found" heading, helper text, "Add Question" button.

---

### Quiz Card

**Structure:**
- White card with border.
- Top area: quiz name (bold) + question count badge (top-right corner).
- Middle: description text (muted, smaller).
- Bottom: action buttons row.

**Variants:**
- **Quiz Builder card** — Edit button (secondary) + Delete button (danger).
- **Exam List card** — "Start Exam" full-width primary button (no Edit/Delete).

---

### Difficulty Badge

**Behaviour:**
- Pill-shaped inline label.
- Values and colours:
  - `Easy` → green text on green-tinted background.
  - `Medium` → amber text on amber-tinted background.
  - `Hard` → red text on red-tinted background.
- Used in: Question table, Question Editor modal, Quiz Create question lists.

---

### Search Box

**Behaviour:**
- Single text input with a search icon on the left (decorative, non-interactive).
- Fires `onChange` on every keystroke; no submit button.
- Filters the associated list in real time.
- Used in: Question Bank (filters question table), Quiz Create "Add Questions" section (filters available question list).

---

### Primary Button

**Behaviour:**
- Solid primary-colour background, white text.
- Used for the main action on each page: Add Question, New Quiz, Save Quiz, Start Exam, Submit, Retry Quiz.
- Hover: darker shade of primary colour.

---

### Secondary Button

**Behaviour:**
- White background, border, dark text.
- Used for Cancel, Back to Exams, Previous (exam navigation).
- Hover: light grey background.

---

### Danger Button

**Behaviour:**
- Used in two contexts: Delete row action (compact, red text on red-tinted background with no explicit border), and confirmation dialogs (solid red background, white text).

---

### Confirmation Dialog

**Behaviour:**
- Appears as a modal overlay covering the full viewport.
- Clicking the backdrop dismisses the dialog (same as Cancel).
- Clicking inside the dialog content does not dismiss it (click propagation stopped).
- Two variants share the same structure:

**Delete Question dialog:**
- Icon, title ("Delete Question"), warning message noting cascade deletion from quizzes.
- Buttons: Cancel (secondary) + Delete (danger primary).
- On confirm: deletes question from the question bank AND removes its ID from all quiz `questionIds` arrays.

**Delete Quiz dialog:**
- Icon, title ("Delete Quiz"), warning message.
- Buttons: Cancel (secondary) + Delete (danger primary).
- On confirm: removes quiz from the quiz list.

---

### Question Editor Modal

**Behaviour:**
- Full-viewport overlay. Clicking the backdrop closes without saving.
- Used for both Add and Edit. Title changes based on mode: "Add Question" / "Edit Question".
- Header is sticky (stays visible when form scrolls).
- Close (×) button in the header dismisses without saving.

**Form Fields (in order):**
1. Question text — textarea, 3 rows, required.
2. Option A — text input, required.
3. Option B — text input, required.
4. Option C — text input, required.
5. Option D — text input, required.
6. Correct Answer — select, values: A | B | C | D.
7. Difficulty — select, values: Easy | Medium | Hard.

**Footer Buttons:**
- Cancel → closes modal, discards changes.
- Save Question → validates (question text must not be empty), then creates or updates the question in state and closes modal.

---

### Empty State

**Structure:**
- Icon in a rounded square.
- Heading (e.g., "No questions found").
- Helper text.
- Optional action button.

**Usage:** Question Bank (no results), Quiz List (no quizzes), Exam List (no quizzes), Quiz Create selected/available lists.

---

### Exam Option Button

**Behaviour:**
- Full-width button inside the question card.
- Displays: letter label (A/B/C/D) in a small rounded square + option text + optional checkmark icon.
- States:
  - **Unselected:** neutral border, white background, grey letter label.
  - **Selected:** primary-colour border, light primary background, primary-colour letter label, checkmark icon visible.
  - **Hover (any state):** light purple tint background, purple border.
- Selecting one option deselects any previously selected option for that question.
- Selections persist when navigating between questions.

---

## Data Fields

### Question

| Field        | Type   | Required | Notes                                         |
| ------------ | ------ | -------- | --------------------------------------------- |
| `id`         | number | yes      | Unique. Assigned as `Date.now()` on creation. |
| `question`   | string | yes      | The question text displayed to the user.      |
| `a`          | string | yes      | Text for option A.                            |
| `b`          | string | yes      | Text for option B.                            |
| `c`          | string | yes      | Text for option C.                            |
| `d`          | string | yes      | Text for option D.                            |
| `correct`    | string | yes      | One of: `"A"`, `"B"`, `"C"`, `"D"`.           |
| `difficulty` | string | yes      | One of: `"Easy"`, `"Medium"`, `"Hard"`.       |

### Quiz

| Field         | Type     | Required | Notes                                              |
| ------------- | -------- | -------- | -------------------------------------------------- |
| `id`          | number   | yes      | Unique. Assigned as `Date.now()` on creation.      |
| `name`        | string   | yes      | Display name for the quiz.                         |
| `description` | string   | no       | Short descriptive text. May be empty.              |
| `questionIds` | number[] | yes      | Ordered list of question IDs included in the quiz. |

### Exam Session State (transient, not persisted)

| Field               | Type                                            | Notes                                      |
| ------------------- | ----------------------------------------------- | ------------------------------------------ |
| `currentExamQuizId` | number \| null                                  | ID of the quiz being taken.                |
| `examQuestion`      | number                                          | Zero-based index of the current question.  |
| `examAnswers`       | `{ [questionIndex]: "A" \| "B" \| "C" \| "D" }` | User's selected answer per question index. |

### Computed / Derived Values

| Value                   | Derivation                                                                   |
| ----------------------- | ---------------------------------------------------------------------------- |
| `examScore`             | Count of `examAnswers[i] === examQs[i].correct` across all questions.        |
| `examPct`               | `Math.round((examScore / examTotal) * 100)`.                                 |
| `qCount` (on quiz card) | `quiz.questionIds` filtered to IDs that still exist in the question bank.    |
| `filteredQuestions`     | `questions` filtered by case-insensitive substring match on `question` text. |

---

## Page Relationships

```
[Question Bank] ←──────────────────────────────── (sidebar)
      │
      └── opens → [Question Editor Modal]
                       └── save/cancel → [Question Bank]

[Quiz Builder: List] ←────────────────────────── (sidebar)
      │
      ├── New Quiz ──→ [Quiz Builder: Create/Edit]
      │                    └── save/cancel → [Quiz Builder: List]
      │
      └── Edit ──────→ [Quiz Builder: Create/Edit]
                           └── save/cancel → [Quiz Builder: List]

[Online Exam: List] ←─────────────────────────── (sidebar)
      │
      └── Start Exam → [Online Exam: Taking]
                           ├── Submit ──→ [Online Exam: Results]
                           │                  ├── Back to Exams → [Online Exam: List]
                           │                  └── Retry Quiz   → [Online Exam: Taking]
                           └── Exit ────→ [Online Exam: List]
```

### Cascade Rules

- **Delete question** → the question is removed from the `questions` array AND its `id` is removed from all `quiz.questionIds` arrays. Quiz question counts update accordingly.
- **Delete quiz** → only removes the quiz; questions in the bank are unaffected.
- **Editing a quiz** → navigates to `quizCreate`; the form is pre-populated with the quiz's current name, description, and selected question IDs.

---

## Responsive Behaviour

- The sidebar is fixed-width (220 px) and does not collapse on any currently targeted viewport.
- The main content area takes all remaining width.
- Quiz cards and Exam cards use a two-column grid; on narrow viewports this should collapse to a single column when the available width cannot accommodate two readable cards.
- The question table columns have fixed widths for Difficulty (96 px) and Actions (96 px); the Question column takes all remaining width and wraps text naturally.
- The Question Editor modal has a fixed width (540 px) and becomes scrollable vertically if its content exceeds the viewport height.
- The Delete confirmation dialogs have a fixed width (360 px) and are always centred in the viewport.
- The Exam Taking and Exam Results content areas are centred with a max-width constraint (600 px and 620 px respectively) and expand to fill narrower viewports.
- The Quiz Create form has a max-width of 720 px.
- No horizontal scrolling is expected in normal use.
