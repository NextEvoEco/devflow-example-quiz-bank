const state = {
  builderQuestionSearch: "",
  currentExamAnswers: {},
  currentExamAttemptId: null,
  currentExamQuestionIndex: 0,
  currentExamQuestions: [],
  currentExamQuizId: null,
  currentExamQuizName: "",
  currentQuizId: null,
  currentPage: "questions",
  editingQuestionId: null,
  examResult: null,
  isSubmitting: false,
  pendingDeleteId: null,
  pendingDeleteType: "question",
  questions: [],
  quizzes: [],
  searchTerm: "",
  selectedQuizQuestionIds: [],
};

const elements = {
  addButton: document.getElementById("add-question-button"),
  backToQuizzesLink: document.getElementById("back-to-quizzes-link"),
  backToExamsButton: document.getElementById("back-to-exams-button"),
  correctInput: document.getElementById("correct-input"),
  count: document.getElementById("question-count"),
  createQuizButton: document.getElementById("create-quiz-button"),
  deleteCancelButton: document.getElementById("delete-cancel-button"),
  deleteConfirmButton: document.getElementById("delete-confirm-button"),
  deleteCopy: document.getElementById("delete-copy"),
  deleteOverlay: document.getElementById("delete-overlay"),
  deleteTitle: document.getElementById("delete-title"),
  difficultyInput: document.getElementById("difficulty-input"),
  editorCancelButton: document.getElementById("editor-cancel-button"),
  editorCloseButton: document.getElementById("editor-close-button"),
  editorOverlay: document.getElementById("editor-overlay"),
  editorSaveButton: document.getElementById("editor-save-button"),
  editorTitle: document.getElementById("editor-title"),
  emptyAddButton: document.getElementById("empty-add-button"),
  emptyCopy: document.getElementById("empty-copy"),
  emptyState: document.getElementById("empty-state"),
  emptyTitle: document.getElementById("empty-title"),
  examCount: document.getElementById("exam-count"),
  examEmptyBuildButton: document.getElementById("exam-empty-build-button"),
  examEmptyState: document.getElementById("exam-empty-state"),
  examGrid: document.getElementById("exam-grid"),
  examExitButton: document.getElementById("exam-exit-button"),
  examNextButton: document.getElementById("exam-next-button"),
  examOptionList: document.getElementById("exam-option-list"),
  examProgressCopy: document.getElementById("exam-progress-copy"),
  examProgressFill: document.getElementById("exam-progress-fill"),
  examQuestionBadge: document.getElementById("exam-question-badge"),
  examQuestionJump: document.getElementById("exam-question-jump"),
  examQuestionTitle: document.getElementById("exam-question-title"),
  examStatusBanner: document.getElementById("exam-status-banner"),
  examTakingStatusBanner: document.getElementById("exam-taking-status-banner"),
  examTakingCopy: document.getElementById("exam-taking-copy"),
  examTakingTitle: document.getElementById("exam-taking-title"),
  examPrevButton: document.getElementById("exam-prev-button"),
  examQuizLabel: document.getElementById("exam-quiz-label"),
  examResultsQuizLabel: document.getElementById("exam-results-quiz-label"),
  examResultsCopy: document.getElementById("exam-results-copy"),
  examResultsTitle: document.getElementById("exam-results-title"),
  examScorePercentage: document.getElementById("exam-score-percentage"),
  examScoreFraction: document.getElementById("exam-score-fraction"),
  examScoreRingFill: document.getElementById("exam-score-ring-fill"),
  examCorrectCount: document.getElementById("exam-correct-count"),
  examIncorrectCount: document.getElementById("exam-incorrect-count"),
  examReviewCount: document.getElementById("exam-review-count"),
  examReviewList: document.getElementById("exam-review-list"),
  form: document.getElementById("question-form"),
  formFeedback: document.getElementById("form-feedback"),
  navExams: document.getElementById("nav-exams"),
  navQuestions: document.getElementById("nav-questions"),
  navQuizzes: document.getElementById("nav-quizzes"),
  optionAInput: document.getElementById("option-a-input"),
  optionBInput: document.getElementById("option-b-input"),
  optionCInput: document.getElementById("option-c-input"),
  optionDInput: document.getElementById("option-d-input"),
  pageViews: document.querySelectorAll("[data-page-view]"),
  questionInput: document.getElementById("question-input"),
  quizBuilderFeedback: document.getElementById("quiz-builder-feedback"),
  quizBuilderForm: document.getElementById("quiz-builder-form"),
  quizBuilderStatusBanner: document.getElementById("quiz-builder-status-banner"),
  quizCount: document.getElementById("quiz-count"),
  quizCreateCopy: document.getElementById("quiz-create-copy"),
  quizCreateMeta: document.getElementById("quiz-create-meta"),
  quizCancelButton: document.getElementById("quiz-cancel-button"),
  quizNameInput: document.getElementById("quiz-name-input"),
  quizPreviewButton: document.getElementById("quiz-preview-button"),
  quizPreviewCloseButton: document.getElementById("quiz-preview-close-button"),
  quizPreviewEmptyCopy: document.getElementById("quiz-preview-empty-copy"),
  quizPreviewPlaceholder: document.getElementById("quiz-preview-placeholder"),
  quizPreviewList: document.getElementById("quiz-preview-list"),
  previewQuestionCount: document.getElementById("preview-question-count"),
  quizSaveButton: document.getElementById("quiz-save-button"),
  quizCreateTitle: document.getElementById("quiz-create-title"),
  quizEmptyCreateButton: document.getElementById("quiz-empty-create-button"),
  quizEmptyState: document.getElementById("quiz-empty-state"),
  quizGrid: document.getElementById("quiz-grid"),
  quizStatusBanner: document.getElementById("quiz-status-banner"),
  selectedEmptyCopy: document.getElementById("selected-empty-copy"),
  selectedQuestionCount: document.getElementById("selected-question-count"),
  selectedQuestionsList: document.getElementById("selected-questions-list"),
  searchInput: document.getElementById("search-input"),
  statusBanner: document.getElementById("status-banner"),
  retryExamButton: document.getElementById("retry-exam-button"),
  resultsBackToExamsButton: document.getElementById("results-back-to-exams-button"),
  table: document.getElementById("question-table"),
  tableBody: document.getElementById("question-table-body"),
  topbarTitle: document.getElementById("topbar-title"),
  builderSearchInput: document.getElementById("builder-search-input"),
  availableQuestionsList: document.getElementById("available-questions-list"),
  availableEmptyCopy: document.getElementById("available-empty-copy"),
  availableQuestionCount: document.getElementById("available-question-count"),
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function difficultyClass(difficulty) {
  return `difficulty-${difficulty.toLowerCase()}`;
}

function setStatus(message) {
  elements.statusBanner.textContent = message;
}

function setQuizStatus(message) {
  elements.quizStatusBanner.textContent = message;
}

function setQuizBuilderStatus(message) {
  elements.quizBuilderStatusBanner.textContent = message;
}

function setExamStatus(message) {
  elements.examStatusBanner.textContent = message;
}

function setExamTakingStatus(message) {
  elements.examTakingStatusBanner.textContent = message;
}

function updateCount() {
  const count = state.questions.length;
  elements.count.textContent = `${count} question${count === 1 ? "" : "s"}`;
}

function updateQuizCount() {
  const count = state.quizzes.length;
  elements.quizCount.textContent = `${count} quiz${count === 1 ? "" : "zes"}`;
}

function updateExamCount() {
  const count = state.quizzes.length;
  elements.examCount.textContent = `${count} exam${count === 1 ? "" : "s"}`;
}

function showFormFeedback(message) {
  elements.formFeedback.textContent = message;
  elements.formFeedback.classList.remove("hidden");
}

function hideFormFeedback() {
  elements.formFeedback.textContent = "";
  elements.formFeedback.classList.add("hidden");
}

function showQuizBuilderFeedback(message) {
  elements.quizBuilderFeedback.textContent = message;
  elements.quizBuilderFeedback.classList.remove("hidden");
}

function hideQuizBuilderFeedback() {
  elements.quizBuilderFeedback.textContent = "";
  elements.quizBuilderFeedback.classList.add("hidden");
}

function resetForm() {
  elements.form.reset();
  elements.correctInput.value = "A";
  elements.difficultyInput.value = "Medium";
  hideFormFeedback();
}

function setCurrentPage(page) {
  state.currentPage = page;

  elements.pageViews.forEach((view) => {
    view.classList.toggle("hidden", view.dataset.pageView !== page);
  });

  elements.navQuestions.classList.toggle("nav-item-active", page === "questions");
  elements.navQuizzes.classList.toggle(
    "nav-item-active",
    page === "quizList" || page === "quizCreate"
  );
  elements.navExams.classList.toggle(
    "nav-item-active",
    page === "examList" || page === "examTaking" || page === "examResults"
  );

  if (page === "questions") {
    elements.topbarTitle.textContent = "Questions";
  } else if (page === "quizList") {
    elements.topbarTitle.textContent = "Quizzes";
  } else if (page === "examList") {
    elements.topbarTitle.textContent = "Available Exams";
  } else if (page === "examTaking") {
    elements.topbarTitle.textContent = "Online Exam";
  } else if (page === "examResults") {
    elements.topbarTitle.textContent = "Exam Results";
  } else {
    elements.topbarTitle.textContent = "Quiz Builder";
  }

  window.location.hash = page;
}

function openEditorModal(question = null) {
  state.editingQuestionId = question ? question.id : null;
  resetForm();

  if (question) {
    elements.editorTitle.textContent = "Edit Question";
    elements.questionInput.value = question.question;
    elements.optionAInput.value = question.a;
    elements.optionBInput.value = question.b;
    elements.optionCInput.value = question.c;
    elements.optionDInput.value = question.d;
    elements.correctInput.value = question.correct;
    elements.difficultyInput.value = question.difficulty;
  } else {
    elements.editorTitle.textContent = "Add Question";
  }

  elements.editorOverlay.classList.remove("hidden");
  elements.questionInput.focus();
}

function closeEditorModal() {
  elements.editorOverlay.classList.add("hidden");
  state.editingQuestionId = null;
  state.isSubmitting = false;
  elements.editorSaveButton.disabled = false;
  resetForm();
}

function openDeleteModal(type, id) {
  state.pendingDeleteType = type;
  state.pendingDeleteId = id;

  if (type === "quiz") {
    const quiz = state.quizzes.find((item) => item.id === id);
    elements.deleteTitle.textContent = "Delete Quiz";
    elements.deleteCopy.textContent = quiz
      ? `Delete "${quiz.name}" from the Quiz List?`
      : "Delete this quiz from the Quiz List?";
  } else {
    const question = state.questions.find((item) => item.id === id);
    elements.deleteTitle.textContent = "Delete Question";
    elements.deleteCopy.textContent = question
      ? `Delete "${question.question}" from the Question Bank? This action cannot be undone in V1.`
      : "Delete this question from the bank? This action cannot be undone in V1.";
  }

  elements.deleteOverlay.classList.remove("hidden");
}

function closeDeleteModal() {
  elements.deleteOverlay.classList.add("hidden");
  state.pendingDeleteId = null;
  state.pendingDeleteType = "question";
  elements.deleteTitle.textContent = "Delete Question";
  elements.deleteCopy.textContent =
    "Delete this question from the bank? This action cannot be undone in V1.";
}

function openQuizBuilderPlaceholder(mode, quiz = null) {
  state.currentQuizId = quiz ? quiz.id : null;
  state.selectedQuizQuestionIds = [];
  state.builderQuestionSearch = "";
  elements.builderSearchInput.value = "";
  elements.quizPreviewPlaceholder.classList.add("hidden");
  hideQuizBuilderFeedback();
  elements.quizNameInput.value = "";
  elements.quizCreateTitle.textContent = mode === "edit" ? "Edit Quiz" : "New Quiz";
  elements.quizCreateCopy.textContent =
    mode === "edit"
      ? "Update the quiz name, adjust selected questions, and preserve the order you want to save."
      : "Create a quiz by naming it, choosing questions, and ordering them before saving.";
  elements.quizCreateMeta.textContent =
    mode === "edit" && quiz
      ? `Editing ${quiz.name}.`
      : "Preview arrives in the next task. Use this button to confirm the selected quiz context.";
  setCurrentPage("quizCreate");
  if (mode === "edit" && quiz) {
    void loadQuizForEditing(quiz.id);
  } else {
    renderQuizBuilder();
    setQuizBuilderStatus("Select at least 3 questions to save a new quiz.");
  }
}

function renderTable() {
  if (state.questions.length === 0) {
    elements.table.classList.add("hidden");
    elements.emptyState.classList.remove("hidden");

    if (state.searchTerm) {
      elements.emptyTitle.textContent = "No questions found";
      elements.emptyCopy.textContent =
        "Try a different keyword or clear the search to view all stored questions.";
    } else {
      elements.emptyTitle.textContent = "No questions yet";
      elements.emptyCopy.textContent = "Start the bank by adding your first question.";
    }
    return;
  }

  elements.table.classList.remove("hidden");
  elements.emptyState.classList.add("hidden");

  elements.tableBody.innerHTML = state.questions
    .map(
      (question) => `
        <tr>
          <td class="question-cell">
            <p class="question-text">${escapeHtml(question.question)}</p>
          </td>
          <td>
            <span class="difficulty-badge ${difficultyClass(question.difficulty)}">
              ${escapeHtml(question.difficulty)}
            </span>
          </td>
          <td>
            <div class="action-group">
              <button class="secondary-button" type="button" data-action="edit-question" data-id="${question.id}">Edit</button>
              <button class="danger-button" type="button" data-action="delete-question" data-id="${question.id}">Del</button>
            </div>
          </td>
        </tr>
      `
    )
    .join("");
}

function renderQuizGrid() {
  if (state.quizzes.length === 0) {
    elements.quizGrid.classList.add("hidden");
    elements.quizEmptyState.classList.remove("hidden");
    return;
  }

  elements.quizGrid.classList.remove("hidden");
  elements.quizEmptyState.classList.add("hidden");
  elements.quizGrid.innerHTML = state.quizzes
    .map(
      (quiz) => `
        <article class="quiz-card">
          <div class="quiz-card-header">
            <h4>${escapeHtml(quiz.name)}</h4>
            <span class="count-badge">${quiz.questionCount} questions</span>
          </div>
          <p class="quiz-card-copy">
            Build, review, and manage this saved quiz from the Quiz Builder workflow.
          </p>
          <div class="action-group">
            <button class="secondary-button" type="button" data-action="edit-quiz" data-id="${quiz.id}">Edit</button>
            <button class="danger-button" type="button" data-action="delete-quiz" data-id="${quiz.id}">Delete</button>
          </div>
        </article>
      `
    )
    .join("");
}

function renderExamGrid() {
  if (state.quizzes.length === 0) {
    elements.examGrid.classList.add("hidden");
    elements.examEmptyState.classList.remove("hidden");
    return;
  }

  elements.examGrid.classList.remove("hidden");
  elements.examEmptyState.classList.add("hidden");
  elements.examGrid.innerHTML = state.quizzes
    .map(
      (quiz) => `
        <article class="quiz-card exam-card">
          <div class="quiz-card-header">
            <h4>${escapeHtml(quiz.name)}</h4>
            <span class="count-badge">${quiz.questionCount} questions</span>
          </div>
          <p class="quiz-card-copy quiz-card-copy-compact">
            Launch this saved quiz as a formal Online Exam. Answers stay hidden until submission.
          </p>
          <button class="primary-button" type="button" data-exam-action="start-exam" data-id="${quiz.id}">
            Start Exam
          </button>
        </article>
      `
    )
    .join("");
}

function resetExamState() {
  state.currentExamAttemptId = null;
  state.currentExamAnswers = {};
  state.currentExamQuestionIndex = 0;
  state.currentExamQuestions = [];
  state.currentExamQuizId = null;
  state.currentExamQuizName = "";
  state.examResult = null;
  elements.examQuizLabel.textContent = "Online Exam";
  elements.examTakingTitle.textContent = "Exam Session";
  elements.examTakingCopy.textContent = "Select a quiz from Available Exams to begin.";
  elements.examResultsQuizLabel.textContent = "Online Exam";
  elements.examResultsTitle.textContent = "Exam Complete!";
  elements.examResultsCopy.textContent =
    "Review the final score and each submitted answer below.";
  elements.examScorePercentage.textContent = "0%";
  elements.examScoreFraction.textContent = "0 / 0";
  elements.examCorrectCount.textContent = "0";
  elements.examIncorrectCount.textContent = "0";
  elements.examReviewCount.textContent = "0 questions";
  elements.examReviewList.innerHTML = "";
  elements.examScoreRingFill.style.stroke = "var(--accent)";
  elements.examScoreRingFill.style.strokeDashoffset = "289";
  setExamTakingStatus("Start an exam to load questions.");
}

function currentExamQuestion() {
  return state.currentExamQuestions[state.currentExamQuestionIndex] ?? null;
}

function renderExamQuestionView() {
  const totalQuestions = state.currentExamQuestions.length;
  const question = currentExamQuestion();
  const questionNumber = totalQuestions === 0 ? 0 : state.currentExamQuestionIndex + 1;

  elements.examQuizLabel.textContent = state.currentExamQuizName || "Online Exam";
  elements.examTakingTitle.textContent = state.currentExamQuizName || "Exam Session";
  elements.examProgressCopy.textContent = `Question ${questionNumber} of ${totalQuestions}`;
  elements.examQuestionBadge.textContent = `Question ${questionNumber}`;
  elements.examProgressFill.style.width =
    totalQuestions === 0 ? "0%" : `${(questionNumber / totalQuestions) * 100}%`;

  elements.examQuestionJump.innerHTML = state.currentExamQuestions
    .map(
      (item, index) => `
        <button
          class="${index === state.currentExamQuestionIndex ? "primary-button" : "secondary-button"} exam-jump-button"
          type="button"
          data-exam-nav="jump"
          data-index="${index}"
        >
          ${index + 1}
        </button>
      `
    )
    .join("");

  if (!question) {
    elements.examQuestionTitle.textContent = "Select a quiz from Available Exams to begin.";
    elements.examOptionList.innerHTML = "";
    elements.examPrevButton.disabled = true;
    elements.examNextButton.disabled = true;
    elements.examNextButton.textContent = "Next";
    return;
  }

  const selectedOption = state.currentExamAnswers[question.id] ?? null;
  elements.examQuestionTitle.textContent = question.question;
  elements.examOptionList.innerHTML = ["A", "B", "C", "D"]
    .map((optionLabel) => {
      const key = optionLabel.toLowerCase();
      const isSelected = selectedOption === optionLabel;
      return `
        <button
          class="exam-option-button ${isSelected ? "exam-option-button-selected" : ""}"
          type="button"
          data-exam-action="select-option"
          data-option="${optionLabel}"
        >
          <span class="exam-option-main">
            <span class="exam-option-label">${optionLabel}</span>
            <span class="exam-option-copy">${escapeHtml(question[key])}</span>
          </span>
          <span class="exam-option-check" aria-hidden="true">${isSelected ? "Selected" : ""}</span>
        </button>
      `;
    })
    .join("");

  elements.examPrevButton.disabled = state.currentExamQuestionIndex === 0;
  elements.examNextButton.disabled = false;
  elements.examNextButton.textContent =
    state.currentExamQuestionIndex === totalQuestions - 1 ? "Submit" : "Next";
}

function scoreRingColor(percentage) {
  if (percentage >= 70) {
    return "var(--easy-text)";
  }
  if (percentage >= 50) {
    return "var(--medium-text)";
  }
  return "var(--hard-text)";
}

function formatAnswerLabel(selectedOption, options) {
  if (!selectedOption) {
    return "Unanswered";
  }

  const optionText = options[selectedOption] ?? "";
  return `${selectedOption}: ${optionText}`;
}

function updateExamResultsPlaceholder() {
  if (!state.examResult) {
    elements.examResultsQuizLabel.textContent = "Online Exam";
    elements.examResultsTitle.textContent = "Exam Complete!";
    elements.examResultsCopy.textContent =
      "Review the final score and each submitted answer below.";
    return;
  }

  const { score, total, percentage, answers } = state.examResult;
  const incorrectCount = Math.max(total - score, 0);
  const circumference = 289;
  const dashOffset = circumference - (circumference * percentage) / 100;

  elements.examResultsQuizLabel.textContent = state.currentExamQuizName || "Online Exam";
  elements.examResultsTitle.textContent = "Exam Complete!";
  elements.examResultsCopy.textContent = `You completed ${state.currentExamQuizName || "this quiz"}. Review the final score and each submitted answer below.`;
  elements.examScorePercentage.textContent = `${percentage}%`;
  elements.examScoreFraction.textContent = `${score} / ${total}`;
  elements.examCorrectCount.textContent = String(score);
  elements.examIncorrectCount.textContent = String(incorrectCount);
  elements.examReviewCount.textContent = `${answers.length} question${
    answers.length === 1 ? "" : "s"
  }`;
  elements.examScoreRingFill.style.stroke = scoreRingColor(percentage);
  elements.examScoreRingFill.style.strokeDashoffset = String(dashOffset);
  elements.examReviewList.innerHTML = answers
    .map((answer, index) => {
      const isCorrect = answer.is_correct;
      const userAnswer = formatAnswerLabel(answer.selected_option, answer.options);
      const correctAnswer = formatAnswerLabel(answer.correct_option, answer.options);
      return `
        <article class="exam-review-card ${
          isCorrect ? "exam-review-card-correct" : "exam-review-card-incorrect"
        }">
          <div class="exam-review-header">
            <div>
              <span class="count-badge">Question ${index + 1}</span>
              <h5 class="exam-review-title">${escapeHtml(answer.question_text)}</h5>
            </div>
            <span class="exam-review-badge ${
              isCorrect ? "exam-review-badge-correct" : "exam-review-badge-incorrect"
            }">
              ${isCorrect ? "Correct" : "Incorrect"}
            </span>
          </div>
          <div class="exam-review-lines">
            <p class="exam-review-line">
              <strong>Your answer:</strong> ${escapeHtml(userAnswer)}
            </p>
            ${
              isCorrect
                ? ""
                : `<p class="exam-review-line exam-review-line-correct">
              <strong>Correct answer:</strong> ${escapeHtml(correctAnswer)}
            </p>`
            }
          </div>
        </article>
      `;
    })
    .join("");
}

function selectedQuestions() {
  return state.selectedQuizQuestionIds
    .map((questionId) => state.questions.find((item) => item.id === questionId))
    .filter(Boolean);
}

function availableQuestions() {
  const selectedIds = new Set(state.selectedQuizQuestionIds);
  return state.questions.filter((question) => {
    if (selectedIds.has(question.id)) {
      return false;
    }
    if (!state.builderQuestionSearch) {
      return true;
    }
    return question.question
      .toLowerCase()
      .includes(state.builderQuestionSearch.toLowerCase());
  });
}

function renderQuizBuilder() {
  const selected = selectedQuestions();
  const available = availableQuestions();

  elements.selectedQuestionCount.textContent = `${selected.length} selected`;
  elements.availableQuestionCount.textContent = `${available.length} available`;

  elements.selectedQuestionsList.innerHTML = selected
    .map(
      (question, index) => `
        <article class="builder-item">
          <div class="builder-item-copy">
            <p class="question-text">${escapeHtml(question.question)}</p>
            <span class="difficulty-badge ${difficultyClass(question.difficulty)}">
              ${escapeHtml(question.difficulty)}
            </span>
          </div>
          <div class="action-group">
            <button class="secondary-button" type="button" data-builder-action="move-up" data-id="${question.id}" ${
              index === 0 ? "disabled" : ""
            }>Up</button>
            <button class="secondary-button" type="button" data-builder-action="move-down" data-id="${question.id}" ${
              index === selected.length - 1 ? "disabled" : ""
            }>Down</button>
            <button class="danger-button" type="button" data-builder-action="remove" data-id="${question.id}">Remove</button>
          </div>
        </article>
      `
    )
    .join("");

  elements.availableQuestionsList.innerHTML = available
    .map(
      (question) => `
        <article class="builder-item">
          <div class="builder-item-copy">
            <p class="question-text">${escapeHtml(question.question)}</p>
            <span class="difficulty-badge ${difficultyClass(question.difficulty)}">
              ${escapeHtml(question.difficulty)}
            </span>
          </div>
          <div class="action-group">
            <button class="primary-button" type="button" data-builder-action="add" data-id="${question.id}">Add</button>
          </div>
        </article>
      `
    )
    .join("");

  elements.selectedEmptyCopy.classList.toggle("hidden", selected.length !== 0);
  elements.availableEmptyCopy.classList.toggle("hidden", available.length !== 0);
  if (!elements.quizPreviewPlaceholder.classList.contains("hidden")) {
    renderQuizPreview();
  }
}

function renderQuizPreview() {
  const selected = selectedQuestions();
  elements.previewQuestionCount.textContent = `${selected.length} question${
    selected.length === 1 ? "" : "s"
  }`;

  elements.quizPreviewList.innerHTML = selected
    .map(
      (question, index) => `
        <article class="preview-card">
          <div class="preview-card-header">
            <span class="count-badge">Question ${index + 1}</span>
            <span class="difficulty-badge ${difficultyClass(question.difficulty)}">
              ${escapeHtml(question.difficulty)}
            </span>
          </div>
          <h5 class="preview-question">${escapeHtml(question.question)}</h5>
          <div class="preview-options">
            ${["a", "b", "c", "d"]
              .map((key, optionIndex) => {
                const optionLabel = String.fromCharCode(65 + optionIndex);
                const isCorrect = question.correct === optionLabel;
                return `
                  <div class="preview-option ${isCorrect ? "preview-option-correct" : ""}">
                    <span class="preview-option-label">${optionLabel}</span>
                    <span>${escapeHtml(question[key])}</span>
                  </div>
                `;
              })
              .join("")}
          </div>
          <p class="preview-answer">
            Correct answer: ${escapeHtml(question.correct)}
          </p>
        </article>
      `
    )
    .join("");

  elements.quizPreviewEmptyCopy.classList.toggle("hidden", selected.length !== 0);
}

async function loadQuestions(searchTerm = "") {
  state.searchTerm = searchTerm;
  setStatus(searchTerm ? "Searching questions..." : "Loading questions...");

  try {
    const query = searchTerm ? `?q=${encodeURIComponent(searchTerm)}` : "";
    const response = await fetch(`/api/questions${query}`);
    if (!response.ok) {
      throw new Error(`Request failed with ${response.status}`);
    }

    const payload = await response.json();
    state.questions = payload.items;
    updateCount();
    renderTable();

    if (state.questions.length === 0) {
      setStatus(searchTerm ? `No matches for "${searchTerm}".` : "Question Bank is empty.");
    } else {
      setStatus(
        searchTerm
          ? `Showing ${state.questions.length} match${
              state.questions.length === 1 ? "" : "es"
            } for "${searchTerm}".`
          : "Question Bank loaded successfully."
      );
    }
  } catch (error) {
    state.questions = [];
    updateCount();
    renderTable();
    setStatus("Unable to load questions right now.");
    console.error(error);
  }
}

async function loadQuizzes() {
  setQuizStatus("Loading quizzes...");

  try {
    const response = await fetch("/api/quizzes");
    if (!response.ok) {
      throw new Error(`Request failed with ${response.status}`);
    }

    const payload = await response.json();
    state.quizzes = payload.items;
    updateQuizCount();
    updateExamCount();
    renderQuizGrid();
    renderExamGrid();
    setQuizStatus(
      state.quizzes.length === 0
        ? "No quizzes have been created yet."
        : "Quiz List loaded successfully."
    );
    setExamStatus(
      state.quizzes.length === 0
        ? "No exams are available until at least one quiz exists."
        : "Available Exams loaded successfully."
    );
  } catch (error) {
    state.quizzes = [];
    updateQuizCount();
    updateExamCount();
    renderQuizGrid();
    renderExamGrid();
    setQuizStatus("Unable to load quizzes right now.");
    setExamStatus("Unable to load available exams right now.");
    console.error(error);
  }
}

async function startExam(quiz) {
  setExamStatus(`Starting "${quiz.name}"...`);
  try {
    const [quizResponse, attemptResponse] = await Promise.all([
      fetch(`/api/quizzes/${quiz.id}`),
      fetch("/api/exams/attempts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ quiz_id: quiz.id }),
      }),
    ]);

    const quizBody = await quizResponse.json();
    const attemptBody = await attemptResponse.json();

    if (!quizResponse.ok) {
      throw new Error(quizBody.error || "Unable to load quiz questions.");
    }
    if (!attemptResponse.ok) {
      throw new Error(attemptBody.error || "Unable to create exam attempt.");
    }

    state.currentExamAttemptId = attemptBody.attempt_id;
    state.currentExamQuizId = quizBody.id;
    state.currentExamQuizName = quizBody.name;
    state.currentExamQuestions = quizBody.questions;
    state.currentExamQuestionIndex = 0;
    state.currentExamAnswers = {};
    state.examResult = null;

    renderExamQuestionView();
    setExamTakingStatus("Exam loaded. Answers save immediately when you select an option.");
    setCurrentPage("examTaking");
  } catch (error) {
    setExamStatus(error.message || "Unable to start the exam.");
  }
}

async function retryCurrentExam() {
  if (state.currentExamQuizId === null) {
    exitExamToList("No exam is available to retry.");
    return;
  }

  const quiz = state.quizzes.find((item) => item.id === state.currentExamQuizId);
  if (!quiz) {
    exitExamToList("The selected quiz is no longer available.");
    return;
  }

  await startExam(quiz);
}

function exitExamToList(message) {
  resetExamState();
  renderExamQuestionView();
  updateExamResultsPlaceholder();
  setCurrentPage("examList");
  if (message) {
    setExamStatus(message);
  }
}

async function saveExamAnswer(optionLabel) {
  const question = currentExamQuestion();
  if (!question || state.currentExamAttemptId === null) {
    return;
  }

  const previousValue = state.currentExamAnswers[question.id] ?? null;
  state.currentExamAnswers = {
    ...state.currentExamAnswers,
    [question.id]: optionLabel,
  };
  renderExamQuestionView();
  setExamTakingStatus(`Saving answer for Question ${state.currentExamQuestionIndex + 1}...`);

  try {
    const response = await fetch(
      `/api/exams/attempts/${state.currentExamAttemptId}/answers/${question.id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ selected_option: optionLabel }),
      }
    );

    if (!response.ok) {
      const body = await response.json();
      throw new Error(body.error || "Unable to save answer.");
    }

    setExamTakingStatus(`Answer saved for Question ${state.currentExamQuestionIndex + 1}.`);
  } catch (error) {
    if (previousValue === null) {
      const nextAnswers = { ...state.currentExamAnswers };
      delete nextAnswers[question.id];
      state.currentExamAnswers = nextAnswers;
    } else {
      state.currentExamAnswers = {
        ...state.currentExamAnswers,
        [question.id]: previousValue,
      };
    }
    renderExamQuestionView();
    setExamTakingStatus(error.message || "Unable to save answer.");
  }
}

function goToExamQuestion(index) {
  if (index < 0 || index >= state.currentExamQuestions.length) {
    return;
  }

  state.currentExamQuestionIndex = index;
  renderExamQuestionView();
  setExamTakingStatus(`Viewing Question ${index + 1} of ${state.currentExamQuestions.length}.`);
}

async function submitExam() {
  if (state.currentExamAttemptId === null) {
    return;
  }

  elements.examNextButton.disabled = true;
  setExamTakingStatus("Submitting exam...");
  try {
    const response = await fetch(
      `/api/exams/attempts/${state.currentExamAttemptId}/submit`,
      {
        method: "POST",
      }
    );
    const body = await response.json();
    if (!response.ok) {
      throw new Error(body.error || "Unable to submit exam.");
    }

    state.examResult = body;
    updateExamResultsPlaceholder();
    setCurrentPage("examResults");
  } catch (error) {
    setExamTakingStatus(error.message || "Unable to submit exam.");
  } finally {
    elements.examNextButton.disabled = false;
  }
}

async function loadQuizForEditing(quizId) {
  setQuizBuilderStatus("Loading quiz...");
  try {
    const response = await fetch(`/api/quizzes/${quizId}`);
    if (!response.ok) {
      const body = await response.json();
      throw new Error(body.error || "Unable to load quiz.");
    }

    const quiz = await response.json();
    state.currentQuizId = quiz.id;
    state.selectedQuizQuestionIds = [...quiz.questionIds];
    elements.quizNameInput.value = quiz.name;
    renderQuizBuilder();
    setQuizBuilderStatus("Quiz loaded. Adjust the name, selection, or order before saving.");
  } catch (error) {
    showQuizBuilderFeedback(error.message || "Unable to load quiz.");
    setQuizBuilderStatus("Unable to load quiz.");
  }
}

function normalizeFormPayload() {
  return {
    question: elements.questionInput.value.trim(),
    a: elements.optionAInput.value.trim(),
    b: elements.optionBInput.value.trim(),
    c: elements.optionCInput.value.trim(),
    d: elements.optionDInput.value.trim(),
    correct: elements.correctInput.value,
    difficulty: elements.difficultyInput.value,
  };
}

function validateFormPayload(payload) {
  const requiredFields = [
    ["question", "Question text is required."],
    ["a", "Option A is required."],
    ["b", "Option B is required."],
    ["c", "Option C is required."],
    ["d", "Option D is required."],
  ];

  for (const [field, message] of requiredFields) {
    if (!payload[field]) {
      return message;
    }
  }

  return null;
}

function moveSelectedQuestion(questionId, direction) {
  const index = state.selectedQuizQuestionIds.indexOf(questionId);
  if (index === -1) {
    return;
  }

  const targetIndex = direction === "up" ? index - 1 : index + 1;
  if (targetIndex < 0 || targetIndex >= state.selectedQuizQuestionIds.length) {
    return;
  }

  const nextIds = [...state.selectedQuizQuestionIds];
  [nextIds[index], nextIds[targetIndex]] = [nextIds[targetIndex], nextIds[index]];
  state.selectedQuizQuestionIds = nextIds;
  renderQuizBuilder();
}

async function submitQuestionForm(event) {
  event.preventDefault();
  if (state.isSubmitting) {
    return;
  }

  const payload = normalizeFormPayload();
  const validationMessage = validateFormPayload(payload);
  if (validationMessage) {
    showFormFeedback(validationMessage);
    return;
  }

  hideFormFeedback();
  state.isSubmitting = true;
  elements.editorSaveButton.disabled = true;

  const isEdit = state.editingQuestionId !== null;
  const url = isEdit
    ? `/api/questions/${state.editingQuestionId}`
    : "/api/questions";
  const method = isEdit ? "PUT" : "POST";

  try {
    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const body = await response.json();
    if (!response.ok) {
      throw new Error(body.error || "Request failed.");
    }

    closeEditorModal();
    await loadQuestions(elements.searchInput.value.trim());
    setStatus(isEdit ? "Question updated successfully." : "Question added successfully.");
  } catch (error) {
    showFormFeedback(error.message || "Unable to save question.");
  } finally {
    state.isSubmitting = false;
    elements.editorSaveButton.disabled = false;
  }
}

async function confirmDelete() {
  if (state.pendingDeleteId === null) {
    return;
  }

  const isQuizDelete = state.pendingDeleteType === "quiz";
  const url = isQuizDelete
    ? `/api/quizzes/${state.pendingDeleteId}`
    : `/api/questions/${state.pendingDeleteId}`;

  try {
    const response = await fetch(url, {
      method: "DELETE",
    });
    const body = await response.json();
    if (!response.ok) {
      throw new Error(body.error || "Delete failed.");
    }

    closeDeleteModal();
    if (isQuizDelete) {
      await loadQuizzes();
      setQuizStatus("Quiz deleted successfully.");
    } else {
      await loadQuestions(elements.searchInput.value.trim());
      setStatus("Question deleted successfully.");
    }
  } catch (error) {
    closeDeleteModal();
    if (isQuizDelete) {
      setQuizStatus(error.message || "Unable to delete quiz.");
    } else {
      setStatus(error.message || "Unable to delete question.");
    }
  }
}

function normalizeQuizPayload() {
  return {
    name: elements.quizNameInput.value.trim(),
    questionIds: [...state.selectedQuizQuestionIds],
  };
}

function validateQuizPayload(payload) {
  if (!payload.name) {
    return "Quiz name is required.";
  }
  if (payload.questionIds.length < 3) {
    return "Select at least 3 questions before saving the quiz.";
  }
  return null;
}

async function submitQuizBuilderForm(event) {
  event.preventDefault();
  const payload = normalizeQuizPayload();
  const validationMessage = validateQuizPayload(payload);
  if (validationMessage) {
    showQuizBuilderFeedback(validationMessage);
    return;
  }

  hideQuizBuilderFeedback();
  elements.quizSaveButton.disabled = true;
  const isEdit = state.currentQuizId !== null;
  const url = isEdit ? `/api/quizzes/${state.currentQuizId}` : "/api/quizzes";
  const method = isEdit ? "PUT" : "POST";

  try {
    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const body = await response.json();
    if (!response.ok) {
      throw new Error(body.error || "Unable to save quiz.");
    }

    await loadQuizzes();
    setCurrentPage("quizList");
    setQuizStatus(isEdit ? "Quiz updated successfully." : "Quiz created successfully.");
  } catch (error) {
    showQuizBuilderFeedback(error.message || "Unable to save quiz.");
    setQuizBuilderStatus("Unable to save quiz.");
  } finally {
    elements.quizSaveButton.disabled = false;
  }
}

function handleBuilderListClick(event) {
  const actionButton = event.target.closest("button[data-builder-action]");
  if (!actionButton) {
    return;
  }

  const questionId = Number(actionButton.dataset.id);
  if (actionButton.dataset.builderAction === "add") {
    if (!state.selectedQuizQuestionIds.includes(questionId)) {
      state.selectedQuizQuestionIds = [...state.selectedQuizQuestionIds, questionId];
      renderQuizBuilder();
    }
    return;
  }

  if (actionButton.dataset.builderAction === "remove") {
    state.selectedQuizQuestionIds = state.selectedQuizQuestionIds.filter((id) => id !== questionId);
    renderQuizBuilder();
    return;
  }

  if (actionButton.dataset.builderAction === "move-up") {
    moveSelectedQuestion(questionId, "up");
    return;
  }

  if (actionButton.dataset.builderAction === "move-down") {
    moveSelectedQuestion(questionId, "down");
  }
}

function handleQuestionTableClick(event) {
  const actionButton = event.target.closest("button[data-action]");
  if (!actionButton) {
    return;
  }

  const questionId = Number(actionButton.dataset.id);
  if (actionButton.dataset.action === "edit-question") {
    const question = state.questions.find((item) => item.id === questionId);
    if (question) {
      openEditorModal(question);
    }
    return;
  }

  if (actionButton.dataset.action === "delete-question") {
    openDeleteModal("question", questionId);
  }
}

function handleQuizGridClick(event) {
  const actionButton = event.target.closest("button[data-action]");
  if (!actionButton) {
    return;
  }

  const quizId = Number(actionButton.dataset.id);
  const quiz = state.quizzes.find((item) => item.id === quizId);
  if (!quiz) {
    return;
  }

  if (actionButton.dataset.action === "edit-quiz") {
    openQuizBuilderPlaceholder("edit", quiz);
    return;
  }

  if (actionButton.dataset.action === "delete-quiz") {
    openDeleteModal("quiz", quizId);
  }
}

function handleExamGridClick(event) {
  const actionButton = event.target.closest("button[data-exam-action]");
  if (!actionButton) {
    return;
  }

  const quizId = Number(actionButton.dataset.id);
  const quiz = state.quizzes.find((item) => item.id === quizId);
  if (!quiz) {
    return;
  }

  if (actionButton.dataset.examAction === "start-exam") {
    void startExam(quiz);
  }
}

function handleExamQuestionClick(event) {
  const navButton = event.target.closest("button[data-exam-nav]");
  if (navButton) {
    goToExamQuestion(Number(navButton.dataset.index));
    return;
  }

  const optionButton = event.target.closest("button[data-exam-action='select-option']");
  if (optionButton) {
    void saveExamAnswer(optionButton.dataset.option);
  }
}

function syncPageFromHash() {
  const hash = window.location.hash.replace("#", "");
  if (hash === "quizList" || hash === "quizCreate" || hash === "examList") {
    setCurrentPage(hash);
  } else if (hash === "examTaking" && state.currentExamQuizId !== null) {
    setCurrentPage("examTaking");
  } else if (hash === "examResults" && state.examResult !== null) {
    setCurrentPage("examResults");
  } else {
    setCurrentPage("questions");
  }
}

function handlePreviewClick() {
  elements.quizPreviewPlaceholder.classList.remove("hidden");
  renderQuizPreview();
  elements.quizCreateMeta.textContent =
    state.selectedQuizQuestionIds.length >= 3
      ? "Preview reflects the current selected question order."
      : "Preview is showing the current in-progress quiz, even before it is valid to save.";
  setQuizBuilderStatus("Quiz preview opened.");
}

function closePreview() {
  elements.quizPreviewPlaceholder.classList.add("hidden");
  setQuizBuilderStatus("Returned to the Quiz Builder.");
}

function bindEvents() {
  elements.searchInput.addEventListener("input", (event) => {
    void loadQuestions(event.target.value.trim());
  });

  elements.navQuestions.addEventListener("click", () => {
    if (state.currentPage === "examTaking" || state.currentPage === "examResults") {
      resetExamState();
      renderExamQuestionView();
      updateExamResultsPlaceholder();
    }
    setCurrentPage("questions");
  });
  elements.navQuizzes.addEventListener("click", () => {
    if (state.currentPage === "examTaking" || state.currentPage === "examResults") {
      resetExamState();
      renderExamQuestionView();
      updateExamResultsPlaceholder();
    }
    setCurrentPage("quizList");
  });
  elements.navExams.addEventListener("click", () => {
    if (state.currentPage === "examTaking" || state.currentPage === "examResults") {
      exitExamToList("Returned to Available Exams.");
      return;
    }
    setCurrentPage("examList");
  });
  elements.addButton.addEventListener("click", () => openEditorModal());
  elements.emptyAddButton.addEventListener("click", () => openEditorModal());
  elements.createQuizButton.addEventListener("click", () => openQuizBuilderPlaceholder("create"));
  elements.quizEmptyCreateButton.addEventListener("click", () => openQuizBuilderPlaceholder("create"));
  elements.examEmptyBuildButton.addEventListener("click", () => setCurrentPage("quizList"));
  elements.backToExamsButton.addEventListener("click", () =>
    exitExamToList("Returned to Available Exams.")
  );
  elements.examExitButton.addEventListener("click", () =>
    exitExamToList("Exam exited before submission.")
  );
  elements.resultsBackToExamsButton.addEventListener("click", () =>
    exitExamToList("Back on Available Exams.")
  );
  elements.retryExamButton.addEventListener("click", () => {
    void retryCurrentExam();
  });
  elements.backToQuizzesLink.addEventListener("click", (event) => {
    event.preventDefault();
    setCurrentPage("quizList");
  });
  elements.quizCancelButton.addEventListener("click", () => setCurrentPage("quizList"));
  elements.quizPreviewButton.addEventListener("click", handlePreviewClick);
  elements.quizPreviewCloseButton.addEventListener("click", closePreview);
  elements.builderSearchInput.addEventListener("input", (event) => {
    state.builderQuestionSearch = event.target.value.trim();
    renderQuizBuilder();
  });
  elements.editorCloseButton.addEventListener("click", closeEditorModal);
  elements.editorCancelButton.addEventListener("click", closeEditorModal);
  elements.deleteCancelButton.addEventListener("click", closeDeleteModal);
  elements.deleteConfirmButton.addEventListener("click", () => {
    void confirmDelete();
  });
  elements.form.addEventListener("submit", (event) => {
    void submitQuestionForm(event);
  });
  elements.tableBody.addEventListener("click", handleQuestionTableClick);
  elements.quizGrid.addEventListener("click", handleQuizGridClick);
  elements.examGrid.addEventListener("click", handleExamGridClick);
  elements.examQuestionJump.addEventListener("click", handleExamQuestionClick);
  elements.examOptionList.addEventListener("click", handleExamQuestionClick);
  elements.examPrevButton.addEventListener("click", () => {
    goToExamQuestion(state.currentExamQuestionIndex - 1);
  });
  elements.examNextButton.addEventListener("click", () => {
    const isLastQuestion =
      state.currentExamQuestionIndex === state.currentExamQuestions.length - 1;
    if (isLastQuestion) {
      void submitExam();
      return;
    }
    goToExamQuestion(state.currentExamQuestionIndex + 1);
  });
  elements.selectedQuestionsList.addEventListener("click", handleBuilderListClick);
  elements.availableQuestionsList.addEventListener("click", handleBuilderListClick);
  elements.quizBuilderForm.addEventListener("submit", (event) => {
    void submitQuizBuilderForm(event);
  });
  window.addEventListener("hashchange", syncPageFromHash);

  elements.editorOverlay.addEventListener("click", (event) => {
    if (event.target === elements.editorOverlay) {
      closeEditorModal();
    }
  });

  elements.deleteOverlay.addEventListener("click", (event) => {
    if (event.target === elements.deleteOverlay) {
      closeDeleteModal();
    }
  });
}

bindEvents();
resetExamState();
renderExamQuestionView();
updateExamResultsPlaceholder();
syncPageFromHash();
void Promise.all([loadQuestions(), loadQuizzes()]);
