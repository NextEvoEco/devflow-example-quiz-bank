import {
  createExamAttempt,
  createQuestion,
  createQuiz,
  deleteQuestion,
  deleteQuiz,
  fetchQuestions,
  fetchQuizzes,
  getQuestion,
  getQuiz,
  saveExamAnswer,
  submitExamAttempt,
  updateQuestion,
  updateQuiz,
} from "./api.js";

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function difficultyClass(difficulty) {
  const normalized = String(difficulty).toLowerCase();
  if (normalized === "easy") return "badge--easy";
  if (normalized === "hard") return "badge--hard";
  return "badge--medium";
}

function renderQuestionRow(question) {
  return `
    <tr>
      <td class="question-table__text">${escapeHtml(question.question)}</td>
      <td>
        <span class="badge ${difficultyClass(question.difficulty)}">
          ${escapeHtml(question.difficulty)}
        </span>
      </td>
      <td class="question-table__actions">
        <button type="button" class="btn btn--secondary btn--small" data-action="edit-question" data-id="${question.id}">
          Edit
        </button>
        <button type="button" class="btn btn--danger btn--small" data-action="delete-question" data-id="${question.id}">
          Del
        </button>
      </td>
    </tr>
  `;
}

function renderExamCard(quiz) {
  return `
    <article class="quiz-card exam-card">
      <div class="quiz-card__header">
        <h3 class="quiz-card__title">${escapeHtml(quiz.name)}</h3>
        <span class="badge badge--count">${quiz.questionCount}</span>
      </div>
      <p class="quiz-card__text">
        ${quiz.questionCount} question${quiz.questionCount === 1 ? "" : "s"} in this exam.
      </p>
      <a
        href="#exam-taking-${quiz.id}"
        class="btn btn--primary exam-card__start"
        data-action="start-exam"
        data-id="${quiz.id}"
      >
        Start Exam
      </a>
    </article>
  `;
}

function resetExamState(quizId) {
  sessionStorage.setItem("currentExamQuizId", String(quizId));
  sessionStorage.setItem("examQuestion", "0");
  sessionStorage.setItem("examAnswers", "{}");
  sessionStorage.removeItem("examAttemptId");
  sessionStorage.removeItem("examResultsPayload");
  sessionStorage.removeItem("examResultsQuizName");
}

function loadExamAnswers() {
  try {
    return JSON.parse(sessionStorage.getItem("examAnswers") || "{}");
  } catch {
    return {};
  }
}

function saveExamAnswersToStorage(answers) {
  sessionStorage.setItem("examAnswers", JSON.stringify(answers));
}

function renderExamOption(label, text, isSelected) {
  return `
    <button
      type="button"
      class="exam-option${isSelected ? " exam-option--selected" : ""}"
      data-option="${label}"
    >
      <span class="exam-option__label">${label}</span>
      <span class="exam-option__text">${escapeHtml(text)}</span>
      ${isSelected ? '<span class="exam-option__check" aria-hidden="true">&#10003;</span>' : ""}
    </button>
  `;
}

function renderQuizCard(quiz) {
  return `
    <article class="quiz-card">
      <div class="quiz-card__header">
        <h3 class="quiz-card__title">${escapeHtml(quiz.name)}</h3>
        <span class="badge badge--count">${quiz.questionCount}</span>
      </div>
      <p class="quiz-card__text">
        ${quiz.questionCount} question${quiz.questionCount === 1 ? "" : "s"} selected.
      </p>
      <div class="quiz-card__actions">
        <a href="#quiz-edit-${quiz.id}" class="btn btn--secondary btn--small" data-action="edit-quiz" data-id="${quiz.id}">
          Edit
        </a>
        <button type="button" class="btn btn--danger btn--small" data-action="delete-quiz" data-id="${quiz.id}">
          Delete
        </button>
      </div>
    </article>
  `;
}

class QuestionEditorModal {
  constructor({ onSaved }) {
    this.modal = document.getElementById("question-editor-modal");
    this.form = document.getElementById("question-editor-form");
    this.title = document.getElementById("question-editor-title");
    this.formError = document.getElementById("question-form-error");
    this.mode = "add";
    this.editingId = null;
    this.onSaved = onSaved;
    this.bindEvents();
  }

  bindEvents() {
    this.form.addEventListener("submit", (event) => {
      event.preventDefault();
      this.submit();
    });

    this.modal.querySelectorAll("[data-close-modal]").forEach((element) => {
      element.addEventListener("click", () => this.close());
    });

    this.modal.querySelector(".modal__dialog").addEventListener("click", (event) => {
      event.stopPropagation();
    });
  }

  clearErrors() {
    this.formError.hidden = true;
    this.formError.textContent = "";
    this.form.querySelectorAll(".field-error").forEach((element) => {
      element.hidden = true;
      element.textContent = "";
    });
    this.form.querySelectorAll(".form-field").forEach((element) => {
      element.classList.remove("form-field--error");
    });
  }

  showErrors(errors = {}, message = "") {
    Object.entries(errors).forEach(([field, text]) => {
      const errorElement = this.form.querySelector(`[data-error-for="${field}"]`);
      const fieldContainer = errorElement?.closest(".form-field");
      if (errorElement) {
        errorElement.textContent = text;
        errorElement.hidden = false;
      }
      fieldContainer?.classList.add("form-field--error");
    });

    if (message) {
      this.formError.textContent = message;
      this.formError.hidden = false;
    }
  }

  getPayload() {
    const formData = new FormData(this.form);
    return {
      question: formData.get("question"),
      a: formData.get("a"),
      b: formData.get("b"),
      c: formData.get("c"),
      d: formData.get("d"),
      correct: formData.get("correct"),
      difficulty: formData.get("difficulty"),
    };
  }

  resetForm() {
    this.form.reset();
    document.getElementById("difficulty").value = "Medium";
    this.clearErrors();
  }

  openAdd() {
    this.mode = "add";
    this.editingId = null;
    this.title.textContent = "Add Question";
    this.resetForm();
    this.modal.hidden = false;
  }

  async openEdit(questionId) {
    this.mode = "edit";
    this.editingId = questionId;
    this.title.textContent = "Edit Question";
    this.resetForm();

    try {
      const question = await getQuestion(questionId);
      this.form.elements.question.value = question.question;
      this.form.elements.a.value = question.a;
      this.form.elements.b.value = question.b;
      this.form.elements.c.value = question.c;
      this.form.elements.d.value = question.d;
      this.form.elements.correct.value = question.correct;
      this.form.elements.difficulty.value = question.difficulty;
      this.modal.hidden = false;
    } catch (error) {
      this.onSaved?.({ error: error.message || "Unable to load question." });
    }
  }

  close() {
    this.modal.hidden = true;
    this.resetForm();
  }

  async submit() {
    this.clearErrors();
    const payload = this.getPayload();

    try {
      if (this.mode === "add") {
        await createQuestion(payload);
      } else {
        await updateQuestion(this.editingId, payload);
      }
      this.close();
      await this.onSaved?.();
    } catch (error) {
      this.showErrors(error.errors, error.message);
    }
  }
}

class DeleteQuestionDialog {
  constructor({ onDeleted }) {
    this.modal = document.getElementById("delete-question-modal");
    this.confirmButton = document.getElementById("confirm-delete-btn");
    this.errorElement = document.getElementById("delete-form-error");
    this.questionId = null;
    this.onDeleted = onDeleted;
    this.bindEvents();
  }

  bindEvents() {
    this.confirmButton.addEventListener("click", () => this.confirm());

    this.modal.querySelectorAll("[data-close-modal]").forEach((element) => {
      element.addEventListener("click", () => this.close());
    });

    this.modal.querySelector(".modal__dialog").addEventListener("click", (event) => {
      event.stopPropagation();
    });
  }

  open(questionId) {
    this.questionId = questionId;
    this.errorElement.hidden = true;
    this.errorElement.textContent = "";
    this.modal.hidden = false;
  }

  close() {
    this.questionId = null;
    this.modal.hidden = true;
  }

  async confirm() {
    if (!this.questionId) {
      return;
    }

    this.errorElement.hidden = true;
    this.errorElement.textContent = "";

    try {
      await deleteQuestion(this.questionId);
      this.close();
      await this.onDeleted?.();
    } catch (error) {
      this.errorElement.textContent = error.message || "Failed to delete question.";
      this.errorElement.hidden = false;
    }
  }
}

class DeleteQuizDialog {
  constructor({ onDeleted }) {
    this.modal = document.getElementById("delete-quiz-modal");
    this.confirmButton = document.getElementById("confirm-delete-quiz-btn");
    this.errorElement = document.getElementById("delete-quiz-error");
    this.quizId = null;
    this.onDeleted = onDeleted;
    this.bindEvents();
  }

  bindEvents() {
    this.confirmButton.addEventListener("click", () => this.confirm());

    this.modal.querySelectorAll("[data-close-quiz-modal]").forEach((element) => {
      element.addEventListener("click", () => this.close());
    });

    this.modal.querySelector(".modal__dialog").addEventListener("click", (event) => {
      event.stopPropagation();
    });
  }

  open(quizId) {
    this.quizId = quizId;
    this.errorElement.hidden = true;
    this.errorElement.textContent = "";
    this.modal.hidden = false;
  }

  close() {
    this.quizId = null;
    this.modal.hidden = true;
  }

  async confirm() {
    if (!this.quizId) {
      return;
    }

    this.errorElement.hidden = true;
    this.errorElement.textContent = "";

    try {
      await deleteQuiz(this.quizId);
      this.close();
      await this.onDeleted?.();
    } catch (error) {
      this.errorElement.textContent = error.message || "Failed to delete quiz.";
      this.errorElement.hidden = false;
    }
  }
}

class QuestionBankPage {
  constructor() {
    this.searchInput = document.getElementById("question-search");
    this.countBadge = document.getElementById("question-count");
    this.table = document.getElementById("question-table");
    this.tableBody = document.getElementById("question-table-body");
    this.emptyState = document.getElementById("questions-empty");
    this.emptyStateText = document.getElementById("empty-state-text");
    this.loadingState = document.getElementById("questions-loading");
    this.errorState = document.getElementById("questions-error");
    this.currentQuery = "";
    this.editorModal = new QuestionEditorModal({
      onSaved: async (result) => {
        if (result?.error) {
          this.setError(result.error);
          return;
        }
        await this.loadQuestions();
      },
    });
    this.deleteDialog = new DeleteQuestionDialog({
      onDeleted: async () => this.loadQuestions(),
    });
  }

  bindEvents() {
    this.searchInput.addEventListener("input", () => {
      this.currentQuery = this.searchInput.value.trim();
      this.loadQuestions();
    });

    document.getElementById("add-question-btn").addEventListener("click", () => {
      this.editorModal.openAdd();
    });

    document.getElementById("empty-add-question-btn").addEventListener("click", () => {
      this.editorModal.openAdd();
    });

    this.tableBody.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button) {
        return;
      }

      const questionId = Number(button.dataset.id);
      if (button.dataset.action === "edit-question") {
        this.editorModal.openEdit(questionId);
      }
      if (button.dataset.action === "delete-question") {
        this.deleteDialog.open(questionId);
      }
    });
  }

  setLoading(isLoading) {
    this.loadingState.hidden = !isLoading;
  }

  setError(message) {
    if (message) {
      this.errorState.textContent = message;
      this.errorState.hidden = false;
      this.table.hidden = true;
      this.emptyState.hidden = true;
      return;
    }

    this.errorState.hidden = true;
    this.errorState.textContent = "";
  }

  render(questions) {
    this.countBadge.textContent = String(questions.length);

    if (questions.length === 0) {
      this.table.hidden = true;
      this.emptyState.hidden = false;
      this.emptyStateText.textContent = this.currentQuery
        ? "No questions match your search."
        : "Add your first question to start building the bank.";
      return;
    }

    this.emptyState.hidden = true;
    this.table.hidden = false;
    this.tableBody.innerHTML = questions.map(renderQuestionRow).join("");
  }

  async loadQuestions() {
    this.setError("");
    this.setLoading(true);

    try {
      const questions = await fetchQuestions(this.currentQuery);
      this.render(questions);
    } catch (error) {
      this.setError(error.message || "Unable to load questions.");
    } finally {
      this.setLoading(false);
    }
  }

  async init() {
    this.bindEvents();
    await this.loadQuestions();
  }
}

class QuizListPage {
  constructor() {
    this.grid = document.getElementById("quiz-grid");
    this.loadingState = document.getElementById("quizzes-loading");
    this.emptyState = document.getElementById("quizzes-empty");
    this.errorState = document.getElementById("quizzes-error");
    this.deleteDialog = new DeleteQuizDialog({
      onDeleted: async () => this.loadQuizzes(),
    });
  }

  bindEvents() {
    this.grid.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button) {
        return;
      }

      if (button.dataset.action === "delete-quiz") {
        this.deleteDialog.open(Number(button.dataset.id));
      }
    });
  }

  setLoading(isLoading) {
    this.loadingState.hidden = !isLoading;
  }

  setError(message) {
    if (message) {
      this.errorState.textContent = message;
      this.errorState.hidden = false;
      this.grid.hidden = true;
      this.emptyState.hidden = true;
      return;
    }

    this.errorState.hidden = true;
    this.errorState.textContent = "";
  }

  render(quizzes) {
    if (quizzes.length === 0) {
      this.grid.hidden = true;
      this.emptyState.hidden = false;
      return;
    }

    this.emptyState.hidden = true;
    this.grid.hidden = false;
    this.grid.innerHTML = quizzes.map(renderQuizCard).join("");
  }

  async loadQuizzes() {
    this.setError("");
    this.setLoading(true);

    try {
      const quizzes = await fetchQuizzes();
      this.render(quizzes);
    } catch (error) {
      this.setError(error.message || "Unable to load quizzes.");
    } finally {
      this.setLoading(false);
    }
  }

  async init() {
    this.bindEvents();
    await this.loadQuizzes();
  }
}

class ExamListPage {
  constructor() {
    this.grid = document.getElementById("exam-grid");
    this.loadingState = document.getElementById("exams-loading");
    this.emptyState = document.getElementById("exams-empty");
    this.errorState = document.getElementById("exams-error");
  }

  bindEvents() {
    this.grid.addEventListener("click", (event) => {
      const startButton = event.target.closest("[data-action='start-exam']");
      if (!startButton) {
        return;
      }

      resetExamState(Number(startButton.dataset.id));
    });
  }

  setLoading(isLoading) {
    this.loadingState.hidden = !isLoading;
  }

  setError(message) {
    if (message) {
      this.errorState.textContent = message;
      this.errorState.hidden = false;
      this.grid.hidden = true;
      this.emptyState.hidden = true;
      return;
    }

    this.errorState.hidden = true;
    this.errorState.textContent = "";
  }

  render(quizzes) {
    if (quizzes.length === 0) {
      this.grid.hidden = true;
      this.emptyState.hidden = false;
      return;
    }

    this.emptyState.hidden = true;
    this.grid.hidden = false;
    this.grid.innerHTML = quizzes.map(renderExamCard).join("");
  }

  async loadExams() {
    this.setError("");
    this.setLoading(true);

    try {
      const quizzes = await fetchQuizzes();
      this.render(quizzes);
    } catch (error) {
      this.setError(error.message || "Unable to load exams.");
    } finally {
      this.setLoading(false);
    }
  }

  async init() {
    this.bindEvents();
    await this.loadExams();
  }
}

const EXAM_RESULTS_PAYLOAD_KEY = "examResultsPayload";
const EXAM_RESULTS_QUIZ_NAME_KEY = "examResultsQuizName";

class ExamTakingPage {
  constructor() {
    this.quizNameEl = document.getElementById("exam-taking-quiz-name");
    this.counterEl = document.getElementById("exam-taking-counter");
    this.progressBar = document.getElementById("exam-progress-bar");
    this.jumpNav = document.getElementById("exam-question-jump");
    this.loadingState = document.getElementById("exam-taking-loading");
    this.errorState = document.getElementById("exam-taking-error");
    this.questionText = document.getElementById("exam-question-text");
    this.optionsContainer = document.getElementById("exam-options");
    this.prevButton = document.getElementById("exam-prev-btn");
    this.nextButton = document.getElementById("exam-next-btn");
    this.quizId = null;
    this.quizName = "";
    this.questions = [];
    this.attemptId = null;
    this.currentIndex = 0;
    this.answers = {};
    this.bindEvents();
  }

  bindEvents() {
    this.prevButton.addEventListener("click", () => this.goToQuestion(this.currentIndex - 1));
    this.nextButton.addEventListener("click", () => this.handleNextOrSubmit());

    this.optionsContainer.addEventListener("click", (event) => {
      const optionButton = event.target.closest("[data-option]");
      if (!optionButton) {
        return;
      }
      this.selectOption(optionButton.dataset.option);
    });

    this.jumpNav.addEventListener("click", (event) => {
      const jumpButton = event.target.closest("[data-jump-index]");
      if (!jumpButton) {
        return;
      }
      this.goToQuestion(Number(jumpButton.dataset.jumpIndex));
    });
  }

  setLoading(isLoading) {
    this.loadingState.hidden = !isLoading;
    this.questionText.hidden = isLoading;
    this.optionsContainer.hidden = isLoading;
  }

  setError(message) {
    if (message) {
      this.errorState.textContent = message;
      this.errorState.hidden = false;
      this.setLoading(false);
      return;
    }

    this.errorState.hidden = true;
    this.errorState.textContent = "";
  }

  getCurrentQuestion() {
    return this.questions[this.currentIndex];
  }

  goToQuestion(index) {
    if (index < 0 || index >= this.questions.length) {
      return;
    }

    this.currentIndex = index;
    sessionStorage.setItem("examQuestion", String(index));
    this.render();
  }

  async selectOption(option) {
    const question = this.getCurrentQuestion();
    if (!question) {
      return;
    }

    this.answers[this.currentIndex] = option;
    saveExamAnswersToStorage(this.answers);
    this.renderQuestionBody();
    this.renderJumpNav();

    try {
      await saveExamAnswer(this.attemptId, question.id, option);
    } catch (error) {
      this.setError(error.message || "Unable to save answer.");
    }
  }

  async handleNextOrSubmit() {
    const isLastQuestion = this.currentIndex === this.questions.length - 1;
    if (isLastQuestion) {
      await this.submitExam();
      return;
    }

    this.goToQuestion(this.currentIndex + 1);
  }

  async submitExam() {
    this.setError("");
    this.nextButton.disabled = true;

    try {
      const result = await submitExamAttempt(this.attemptId);
      sessionStorage.setItem(EXAM_RESULTS_PAYLOAD_KEY, JSON.stringify(result));
      sessionStorage.setItem(EXAM_RESULTS_QUIZ_NAME_KEY, this.quizName);
      window.location.hash = `#exam-results-${this.quizId}`;
    } catch (error) {
      this.setError(error.message || "Unable to submit exam.");
      this.nextButton.disabled = false;
    }
  }

  renderJumpNav() {
    this.jumpNav.innerHTML = this.questions
      .map((_, index) => {
        const classes = ["exam-jump-btn"];
        if (index === this.currentIndex) {
          classes.push("exam-jump-btn--active");
        }
        if (this.answers[index]) {
          classes.push("exam-jump-btn--answered");
        }
        return `
          <button
            type="button"
            class="${classes.join(" ")}"
            data-jump-index="${index}"
            aria-label="Go to question ${index + 1}"
          >
            ${index + 1}
          </button>
        `;
      })
      .join("");
  }

  renderQuestionBody() {
    const question = this.getCurrentQuestion();
    if (!question) {
      return;
    }

    const selectedOption = this.answers[this.currentIndex];
    this.questionText.textContent = question.question;
    this.optionsContainer.innerHTML = ["A", "B", "C", "D"]
      .map((label) =>
        renderExamOption(label, question[label.toLowerCase()], selectedOption === label),
      )
      .join("");
  }

  render() {
    const total = this.questions.length;
    const position = this.currentIndex + 1;
    this.counterEl.textContent = `Question ${position} of ${total}`;
    this.progressBar.style.width = `${(position / total) * 100}%`;
    this.prevButton.disabled = this.currentIndex === 0;
    this.nextButton.textContent = this.currentIndex === total - 1 ? "Submit" : "Next";
    this.nextButton.disabled = false;
    this.renderJumpNav();
    this.renderQuestionBody();
  }

  async load(quizId) {
    this.setError("");
    this.setLoading(true);
    this.quizId = quizId;

    try {
      const quiz = await getQuiz(quizId);
      this.quizName = quiz.name;
      this.questions = quiz.questions ?? [];
      this.quizNameEl.textContent = quiz.name;

      if (this.questions.length === 0) {
        throw new Error("This quiz has no questions.");
      }

      this.attemptId = await createExamAttempt(quizId);
      sessionStorage.setItem("examAttemptId", String(this.attemptId));
      sessionStorage.setItem("currentExamQuizId", String(quizId));

      this.answers = loadExamAnswers();
      const storedIndex = Number(sessionStorage.getItem("examQuestion") || "0");
      this.currentIndex = Number.isFinite(storedIndex)
        ? Math.min(Math.max(storedIndex, 0), this.questions.length - 1)
        : 0;

      this.setLoading(false);
      this.render();
    } catch (error) {
      this.setError(error.message || "Unable to load exam.");
    }
  }
}

class ExamResultsPage {
  constructor() {
    this.quizNameEl = document.getElementById("exam-results-quiz-name");
    this.scoreSummary = document.getElementById("exam-results-score-summary");
    this.correctCountEl = document.getElementById("exam-results-correct-count");
    this.incorrectCountEl = document.getElementById("exam-results-incorrect-count");
    this.reviewList = document.getElementById("exam-results-review-list");
    this.retryButton = document.getElementById("exam-results-retry-btn");
    this.quizId = null;
    this.bindEvents();
  }

  bindEvents() {
    this.retryButton.addEventListener("click", () => {
      if (!this.quizId) {
        return;
      }
      resetExamState(this.quizId);
      window.location.hash = `#exam-taking-${this.quizId}`;
    });
  }

  load(quizId) {
    const payload = sessionStorage.getItem(EXAM_RESULTS_PAYLOAD_KEY);
    if (!payload) {
      window.location.hash = "#exams";
      return;
    }

    const result = JSON.parse(payload);
    const quizName = sessionStorage.getItem(EXAM_RESULTS_QUIZ_NAME_KEY) || `Quiz ${quizId}`;
    this.quizId = quizId;
    this.quizNameEl.textContent = quizName;
    this.correctCountEl.textContent = String(result.score);
    this.incorrectCountEl.textContent = String(result.total - result.score);
    this.scoreSummary.innerHTML = renderScoreRing(
      result.percentage,
      result.score,
      result.total,
    );
    this.reviewList.innerHTML = result.answers
      .map((answer, index) => renderAnswerReviewItem(answer, index))
      .join("");
  }
}

function scoreRingColor(percentage) {
  if (percentage >= 70) {
    return "#22a06b";
  }
  if (percentage >= 50) {
    return "#d97706";
  }
  return "#dc3545";
}

function renderScoreRing(percentage, score, total) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;
  const color = scoreRingColor(percentage);

  return `
    <svg class="exam-score-ring" viewBox="0 0 140 140" aria-hidden="true">
      <circle class="exam-score-ring__track" cx="70" cy="70" r="${radius}"></circle>
      <circle
        class="exam-score-ring__progress"
        cx="70"
        cy="70"
        r="${radius}"
        style="stroke: ${color}; stroke-dasharray: ${circumference}; stroke-dashoffset: ${offset};"
      ></circle>
    </svg>
    <div class="exam-score-ring__label">
      <strong>${percentage}%</strong>
      <span>${score} / ${total}</span>
    </div>
  `;
}

function formatAnswerOption(answer, option) {
  if (!option) {
    return "No answer";
  }
  return `${option}: ${answer[option.toLowerCase()]}`;
}

function renderAnswerReviewItem(answer, index) {
  const statusClass = answer.is_correct
    ? "exam-review-item--correct"
    : "exam-review-item--incorrect";
  const icon = answer.is_correct ? "&#10003;" : "&#10007;";
  const yourAnswer = formatAnswerOption(answer, answer.selected_option);
  const correctLine = answer.is_correct
    ? ""
    : `<span class="exam-review-item__correct"> · Correct: ${escapeHtml(formatAnswerOption(answer, answer.correct_option))}</span>`;

  return `
    <article class="exam-review-item ${statusClass}">
      <div class="exam-review-item__icon" aria-hidden="true">${icon}</div>
      <div class="exam-review-item__body">
        <p class="exam-review-item__question">${index + 1}. ${escapeHtml(answer.question_text)}</p>
        <p class="exam-review-item__answers">
          Your answer: ${escapeHtml(yourAnswer)}${correctLine}
        </p>
        <span class="exam-review-item__badge">${answer.is_correct ? "Correct" : "Incorrect"}</span>
      </div>
    </article>
  `;
}

const MIN_QUIZ_QUESTIONS = 3;
const QUIZ_PREVIEW_DRAFT_KEY = "quizPreviewDraft";
const QUIZ_PREVIEW_RETURN_KEY = "quizPreviewReturnHash";

class QuizBuilderPage {
  constructor() {
    this.title = document.getElementById("quiz-builder-title");
    this.nameInput = document.getElementById("quiz-name-input");
    this.selectedList = document.getElementById("quiz-selected-list");
    this.selectedCount = document.getElementById("quiz-selected-count");
    this.selectedEmpty = document.getElementById("quiz-selected-empty");
    this.availableList = document.getElementById("quiz-available-list");
    this.availableEmpty = document.getElementById("quiz-available-empty");
    this.formError = document.getElementById("quiz-builder-error");
    this.previewButton = document.getElementById("quiz-preview-btn");
    this.saveButton = document.getElementById("quiz-save-btn");
    this.mode = "create";
    this.quizId = null;
    this.selectedQuestions = [];
    this.allQuestions = [];
    this.bindEvents();
  }

  bindEvents() {
    this.saveButton.addEventListener("click", () => this.save());
    this.previewButton.addEventListener("click", () => this.openPreview());

    this.selectedList.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button) {
        return;
      }

      const index = Number(button.dataset.index);
      if (button.dataset.action === "remove-selected") {
        this.removeSelected(index);
      }
      if (button.dataset.action === "move-up") {
        this.moveSelected(index, -1);
      }
      if (button.dataset.action === "move-down") {
        this.moveSelected(index, 1);
      }
    });

    this.availableList.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-action='add-available']");
      if (!button) {
        return;
      }
      this.addSelected(Number(button.dataset.id));
    });
  }

  clearError() {
    this.formError.hidden = true;
    this.formError.textContent = "";
  }

  showError(message) {
    this.formError.textContent = message;
    this.formError.hidden = false;
  }

  reset() {
    this.mode = "create";
    this.quizId = null;
    this.selectedQuestions = [];
    this.allQuestions = [];
    this.nameInput.value = "";
    this.clearError();
    this.render();
  }

  restoreFromDraftIfAvailable({ mode, quizId = null }) {
    const draftRaw = sessionStorage.getItem(QUIZ_PREVIEW_DRAFT_KEY);
    if (!draftRaw) {
      return false;
    }

    const draft = JSON.parse(draftRaw);
    if (mode === "create" && draft.quizId) {
      return false;
    }
    if (mode === "edit" && draft.quizId !== quizId) {
      return false;
    }

    this.nameInput.value = draft.name || "";
    this.selectedQuestions = [...draft.questions];
    return true;
  }

  async loadCreate() {
    this.reset();
    this.title.textContent = "New Quiz";
    this.allQuestions = await fetchQuestions();
    this.restoreFromDraftIfAvailable({ mode: "create" });
    this.render();
  }

  async loadEdit(quizId) {
    this.clearError();
    this.mode = "edit";
    this.quizId = quizId;
    this.title.textContent = "Edit Quiz";
    this.allQuestions = await fetchQuestions();

    if (!this.restoreFromDraftIfAvailable({ mode: "edit", quizId })) {
      const quiz = await getQuiz(quizId);
      this.nameInput.value = quiz.name;
      this.selectedQuestions = [...quiz.questions];
    }

    this.render();
  }

  getAvailableQuestions() {
    const selectedIds = new Set(this.selectedQuestions.map((question) => question.id));
    return this.allQuestions.filter((question) => !selectedIds.has(question.id));
  }

  renderSelectedRow(question, index) {
    const isFirst = index === 0;
    const isLast = index === this.selectedQuestions.length - 1;

    return `
      <li class="builder-row">
        <div class="builder-row__content">
          <p class="builder-row__text">${escapeHtml(question.question)}</p>
          <span class="badge ${difficultyClass(question.difficulty)}">
            ${escapeHtml(question.difficulty)}
          </span>
        </div>
        <div class="builder-row__actions">
          <button type="button" class="btn btn--secondary btn--small" data-action="move-up" data-index="${index}" ${isFirst ? "disabled" : ""} aria-label="Move up">&#8593;</button>
          <button type="button" class="btn btn--secondary btn--small" data-action="move-down" data-index="${index}" ${isLast ? "disabled" : ""} aria-label="Move down">&#8595;</button>
          <button type="button" class="btn btn--danger btn--small" data-action="remove-selected" data-index="${index}" aria-label="Remove">&#215;</button>
        </div>
      </li>
    `;
  }

  renderAvailableRow(question) {
    return `
      <li class="builder-row">
        <div class="builder-row__content">
          <p class="builder-row__text">${escapeHtml(question.question)}</p>
          <span class="badge ${difficultyClass(question.difficulty)}">
            ${escapeHtml(question.difficulty)}
          </span>
        </div>
        <div class="builder-row__actions">
          <button type="button" class="btn btn--secondary btn--small" data-action="add-available" data-id="${question.id}">
            Add
          </button>
        </div>
      </li>
    `;
  }

  render() {
    this.selectedCount.textContent = String(this.selectedQuestions.length);

    if (this.selectedQuestions.length === 0) {
      this.selectedEmpty.hidden = false;
      this.selectedList.hidden = true;
      this.selectedList.innerHTML = "";
    } else {
      this.selectedEmpty.hidden = true;
      this.selectedList.hidden = false;
      this.selectedList.innerHTML = this.selectedQuestions
        .map((question, index) => this.renderSelectedRow(question, index))
        .join("");
    }

    const availableQuestions = this.getAvailableQuestions();
    if (availableQuestions.length === 0) {
      this.availableEmpty.hidden = false;
      this.availableList.hidden = true;
      this.availableList.innerHTML = "";
    } else {
      this.availableEmpty.hidden = true;
      this.availableList.hidden = false;
      this.availableList.innerHTML = availableQuestions
        .map((question) => this.renderAvailableRow(question))
        .join("");
    }
  }

  addSelected(questionId) {
    const question = this.allQuestions.find((item) => item.id === questionId);
    if (!question || this.selectedQuestions.some((item) => item.id === questionId)) {
      return;
    }
    this.selectedQuestions.push(question);
    this.clearError();
    this.render();
  }

  removeSelected(index) {
    this.selectedQuestions.splice(index, 1);
    this.clearError();
    this.render();
  }

  moveSelected(index, direction) {
    const targetIndex = index + direction;
    if (targetIndex < 0 || targetIndex >= this.selectedQuestions.length) {
      return;
    }

    const updated = [...this.selectedQuestions];
    const [moved] = updated.splice(index, 1);
    updated.splice(targetIndex, 0, moved);
    this.selectedQuestions = updated;
    this.render();
  }

  getPayload() {
    return {
      name: this.nameInput.value.trim(),
      questionIds: this.selectedQuestions.map((question) => question.id),
    };
  }

  validatePayload(payload) {
    if (!payload.name) {
      this.showError("Quiz name is required.");
      return false;
    }
    if (payload.questionIds.length < MIN_QUIZ_QUESTIONS) {
      this.showError(`A quiz must include at least ${MIN_QUIZ_QUESTIONS} questions.`);
      return false;
    }
    return true;
  }

  async save() {
    const payload = this.getPayload();
    if (!this.validatePayload(payload)) {
      return;
    }

    try {
      if (this.mode === "create") {
        await createQuiz(payload);
      } else {
        await updateQuiz(this.quizId, payload);
      }
      window.location.hash = "#quizzes";
    } catch (error) {
      const message =
        error.errors?.questionIds ||
        error.errors?.name ||
        error.message ||
        "Unable to save quiz.";
      this.showError(message);
    }
  }

  openPreview() {
    const payload = this.getPayload();
    if (payload.questionIds.length < MIN_QUIZ_QUESTIONS) {
      this.showError(`Select at least ${MIN_QUIZ_QUESTIONS} questions to preview the quiz.`);
      return;
    }

    sessionStorage.setItem(
      QUIZ_PREVIEW_DRAFT_KEY,
      JSON.stringify({
        name: payload.name || "Untitled Quiz",
        questions: this.selectedQuestions,
        quizId: this.quizId,
      }),
    );
    sessionStorage.setItem(
      QUIZ_PREVIEW_RETURN_KEY,
      this.mode === "edit" ? `#quiz-edit-${this.quizId}` : "#quiz-create",
    );

    if (this.mode === "edit" && this.quizId) {
      window.location.hash = `#quiz-preview-${this.quizId}`;
      return;
    }

    window.location.hash = "#quiz-preview-draft";
  }
}

function renderPreviewOption(label, text, isCorrect) {
  return `
    <li class="preview-option${isCorrect ? " preview-option--correct" : ""}">
      <span>
        <span class="preview-option__label">${label}.</span>
        ${escapeHtml(text)}
      </span>
      ${isCorrect ? '<span class="preview-option__mark">Correct answer</span>' : ""}
    </li>
  `;
}

function renderPreviewQuestion(question, index) {
  const options = [
    { label: "A", text: question.a },
    { label: "B", text: question.b },
    { label: "C", text: question.c },
    { label: "D", text: question.d },
  ];

  return `
    <article class="preview-question">
      <h3 class="preview-question__title">Question ${index + 1}</h3>
      <p class="preview-question__text">${escapeHtml(question.question)}</p>
      <ul class="preview-options">
        ${options
          .map((option) =>
            renderPreviewOption(
              option.label,
              option.text,
              question.correct === option.label,
            ),
          )
          .join("")}
      </ul>
    </article>
  `;
}

class QuizPreviewPage {
  constructor() {
    this.title = document.getElementById("quiz-preview-title");
    this.content = document.getElementById("quiz-preview-content");
    this.errorState = document.getElementById("quiz-preview-error");
    this.backLink = document.getElementById("quiz-preview-back-link");
    this.bindEvents();
  }

  bindEvents() {
    this.backLink.addEventListener("click", (event) => {
      event.preventDefault();
      const returnHash = sessionStorage.getItem(QUIZ_PREVIEW_RETURN_KEY) || "#quiz-create";
      window.location.hash = returnHash;
    });
  }

  setError(message) {
    this.errorState.textContent = message;
    this.errorState.hidden = false;
    this.content.innerHTML = "";
  }

  clearError() {
    this.errorState.hidden = true;
    this.errorState.textContent = "";
  }

  render(preview) {
    this.clearError();
    this.title.textContent = preview.name || "Quiz Preview";
    this.content.innerHTML = preview.questions
      .map((question, index) => renderPreviewQuestion(question, index))
      .join("");
  }

  loadDraftFromStorage(route) {
    const draftRaw = sessionStorage.getItem(QUIZ_PREVIEW_DRAFT_KEY);
    if (!draftRaw) {
      return null;
    }

    const draft = JSON.parse(draftRaw);
    if (route.previewMode === "draft") {
      return draft;
    }

    if (route.previewMode === "id" && draft.quizId === route.quizId) {
      return draft;
    }

    return null;
  }

  async load(route) {
    const returnHash = sessionStorage.getItem(QUIZ_PREVIEW_RETURN_KEY) || "#quiz-create";
    this.backLink.href = returnHash;

    const draftPreview = this.loadDraftFromStorage(route);
    if (draftPreview) {
      this.render(draftPreview);
      return;
    }

    if (route.previewMode === "id") {
      const quiz = await getQuiz(route.quizId);
      this.render({ name: quiz.name, questions: quiz.questions });
      return;
    }

    this.setError("Unable to load quiz preview.");
  }
}

class AppRouter {
  constructor({
    questionPage,
    quizPage,
    quizBuilderPage,
    quizPreviewPage,
    examPage,
    examTakingPage,
    examResultsPage,
  }) {
    this.questionPage = questionPage;
    this.quizPage = quizPage;
    this.quizBuilderPage = quizBuilderPage;
    this.quizPreviewPage = quizPreviewPage;
    this.examPage = examPage;
    this.examTakingPage = examTakingPage;
    this.examResultsPage = examResultsPage;
    this.topbarTitle = document.getElementById("topbar-title");
    this.pages = new Map(
      Array.from(document.querySelectorAll("[data-page]")).map((element) => [
        element.dataset.page,
        element,
      ]),
    );
    this.navItems = Array.from(document.querySelectorAll("[data-nav-page]"));
  }

  parseRoute() {
    const hash = window.location.hash || "#questions";
    if (hash === "#questions") {
      return { page: "questions", title: "Question Bank" };
    }
    if (hash === "#quizzes") {
      return { page: "quizzes", title: "Quiz Builder" };
    }
    if (hash === "#quiz-create") {
      return { page: "quiz-builder", title: "Quiz Builder", mode: "create" };
    }
    if (hash.startsWith("#quiz-edit-")) {
      return {
        page: "quiz-builder",
        title: "Quiz Builder",
        mode: "edit",
        quizId: Number(hash.replace("#quiz-edit-", "")),
      };
    }
    if (hash === "#quiz-preview-draft") {
      return { page: "quiz-preview", title: "Quiz Builder", previewMode: "draft" };
    }
    if (hash.startsWith("#quiz-preview-")) {
      return {
        page: "quiz-preview",
        title: "Quiz Builder",
        previewMode: "id",
        quizId: Number(hash.replace("#quiz-preview-", "")),
      };
    }
    if (hash === "#exams") {
      return { page: "exams", title: "Online Exam" };
    }
    if (hash.startsWith("#exam-taking-")) {
      return {
        page: "exam-taking",
        title: "Online Exam",
        quizId: Number(hash.replace("#exam-taking-", "")),
      };
    }
    if (hash.startsWith("#exam-results-")) {
      return {
        page: "exam-results",
        title: "Online Exam",
        quizId: Number(hash.replace("#exam-results-", "")),
      };
    }
    return { page: "questions", title: "Question Bank" };
  }

  isQuizBuilderRoute(page) {
    return page === "quizzes" || page === "quiz-builder" || page === "quiz-preview";
  }

  isOnlineExamRoute(page) {
    return page === "exams" || page === "exam-taking" || page === "exam-results";
  }

  async handleRouteChange() {
    const route = this.parseRoute();
    this.topbarTitle.textContent = route.title;

    for (const [page, element] of this.pages.entries()) {
      element.hidden = page !== route.page;
    }

    this.navItems.forEach((element) => {
      const navPage = element.dataset.navPage;
      const isActive =
        (route.page === "questions" && navPage === "questions") ||
        (this.isQuizBuilderRoute(route.page) && navPage === "quizzes") ||
        (this.isOnlineExamRoute(route.page) && navPage === "exams");
      element.classList.toggle("sidebar__item--active", isActive);
    });

    if (route.page === "questions") {
      await this.questionPage.loadQuestions();
    }
    if (route.page === "quizzes") {
      await this.quizPage.loadQuizzes();
    }
    if (route.page === "quiz-builder") {
      try {
        if (route.mode === "edit") {
          await this.quizBuilderPage.loadEdit(route.quizId);
        } else {
          await this.quizBuilderPage.loadCreate();
        }
      } catch (error) {
        this.quizBuilderPage.showError(error.message || "Unable to load quiz builder.");
      }
    }
    if (route.page === "quiz-preview") {
      try {
        await this.quizPreviewPage.load(route);
      } catch (error) {
        this.quizPreviewPage.setError(error.message || "Unable to load quiz preview.");
      }
    }
    if (route.page === "exams") {
      await this.examPage.loadExams();
    }
    if (route.page === "exam-taking") {
      try {
        await this.examTakingPage.load(route.quizId);
      } catch (error) {
        this.examTakingPage.setError(error.message || "Unable to load exam session.");
      }
    }
    if (route.page === "exam-results") {
      this.examResultsPage.load(route.quizId);
    }
  }

  bindEvents() {
    window.addEventListener("hashchange", () => {
      this.handleRouteChange();
    });
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const questionPage = new QuestionBankPage();
  const quizPage = new QuizListPage();
  const quizBuilderPage = new QuizBuilderPage();
  const quizPreviewPage = new QuizPreviewPage();
  const examPage = new ExamListPage();
  const examTakingPage = new ExamTakingPage();
  const examResultsPage = new ExamResultsPage();
  questionPage.bindEvents();
  quizPage.bindEvents();
  examPage.bindEvents();

  const router = new AppRouter({
    questionPage,
    quizPage,
    quizBuilderPage,
    quizPreviewPage,
    examPage,
    examTakingPage,
    examResultsPage,
  });
  router.bindEvents();
  await router.handleRouteChange();
});
