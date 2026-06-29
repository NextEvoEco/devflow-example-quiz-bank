const MIN_QUIZ_QUESTIONS = 3;

const builderState = {
  mode: "create",
  quizId: null,
  name: "",
  allQuestions: [],
  selectedQuestions: [],
  isLoading: false,
};

const builderElements = {
  title: document.getElementById("quiz-builder-title"),
  status: document.getElementById("quiz-builder-status"),
  error: document.getElementById("quiz-builder-error"),
  nameInput: document.getElementById("quiz-name-input"),
  selectedList: document.getElementById("selected-questions-list"),
  selectedEmpty: document.getElementById("selected-questions-empty"),
  selectedCount: document.getElementById("selected-question-count"),
  availableList: document.getElementById("available-questions-list"),
  availableEmpty: document.getElementById("available-questions-empty"),
  formError: document.getElementById("quiz-builder-form-error"),
  backBtn: document.getElementById("quiz-builder-back-btn"),
  cancelBtn: document.getElementById("quiz-builder-cancel-btn"),
  previewBtn: document.getElementById("quiz-builder-preview-btn"),
  saveBtn: document.getElementById("quiz-builder-save-btn"),
  previewModal: document.getElementById("quiz-preview-modal"),
  previewContent: document.getElementById("quiz-preview-content"),
  previewCloseBtn: document.getElementById("quiz-preview-close-btn"),
  previewDoneBtn: document.getElementById("quiz-preview-done-btn"),
};

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function difficultyClass(difficulty) {
  return `difficulty-badge difficulty-${difficulty.toLowerCase()}`;
}

async function parseApiResponse(response) {
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = payload.error || `Request failed (${response.status})`;
    throw new Error(message);
  }
  return payload;
}

async function fetchAllQuestions() {
  const response = await fetch("/api/questions");
  const payload = await parseApiResponse(response);
  return payload.questions ?? [];
}

async function fetchQuiz(quizId) {
  const response = await fetch(`/api/quizzes/${quizId}`);
  return parseApiResponse(response);
}

async function createQuiz(payload) {
  const response = await fetch("/api/quizzes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseApiResponse(response);
}

async function updateQuiz(quizId, payload) {
  const response = await fetch(`/api/quizzes/${quizId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseApiResponse(response);
}

function setBuilderLoading(isLoading) {
  builderState.isLoading = isLoading;
  if (builderElements.status) {
    builderElements.status.hidden = !isLoading;
  }
}

function setBuilderError(message) {
  if (!builderElements.error) {
    return;
  }
  builderElements.error.hidden = !message;
  builderElements.error.textContent = message;
}

function setFormError(message) {
  if (!builderElements.formError) {
    return;
  }
  builderElements.formError.hidden = !message;
  builderElements.formError.textContent = message;
}

function getSelectedQuestionIds() {
  return builderState.selectedQuestions.map((question) => question.id);
}

function getAvailableQuestions() {
  const selectedIds = new Set(getSelectedQuestionIds());
  return builderState.allQuestions.filter((question) => !selectedIds.has(question.id));
}

function renderSelectedQuestionRow(question, index, total) {
  return `
    <article class="builder-row" data-question-id="${question.id}">
      <div class="builder-row-main">
        <p class="builder-row-text">${escapeHtml(question.question)}</p>
        <span class="${difficultyClass(question.difficulty)}">${escapeHtml(question.difficulty)}</span>
      </div>
      <div class="builder-row-actions">
        <button class="btn btn-secondary btn-compact" type="button" data-action="up" ${index === 0 ? "disabled" : ""}>Up</button>
        <button class="btn btn-secondary btn-compact" type="button" data-action="down" ${index === total - 1 ? "disabled" : ""}>Down</button>
        <button class="btn btn-danger btn-compact" type="button" data-action="remove">Remove</button>
      </div>
    </article>
  `;
}

function renderAvailableQuestionRow(question) {
  return `
    <article class="builder-row" data-question-id="${question.id}">
      <div class="builder-row-main">
        <p class="builder-row-text">${escapeHtml(question.question)}</p>
        <span class="${difficultyClass(question.difficulty)}">${escapeHtml(question.difficulty)}</span>
      </div>
      <div class="builder-row-actions">
        <button class="btn btn-secondary btn-compact" type="button" data-action="add">Add</button>
      </div>
    </article>
  `;
}

function renderBuilderPanels() {
  const selectedCount = builderState.selectedQuestions.length;
  const availableQuestions = getAvailableQuestions();

  if (builderElements.selectedCount) {
    builderElements.selectedCount.textContent = String(selectedCount);
  }

  if (builderElements.selectedList) {
    builderElements.selectedList.innerHTML = builderState.selectedQuestions
      .map((question, index) =>
        renderSelectedQuestionRow(question, index, builderState.selectedQuestions.length)
      )
      .join("");
  }

  if (builderElements.selectedEmpty) {
    builderElements.selectedEmpty.hidden = selectedCount > 0;
  }

  if (builderElements.availableList) {
    builderElements.availableList.innerHTML = availableQuestions
      .map((question) => renderAvailableQuestionRow(question))
      .join("");
  }

  if (builderElements.availableEmpty) {
    builderElements.availableEmpty.hidden = availableQuestions.length > 0;
  }
}

function resetBuilderState() {
  builderState.mode = "create";
  builderState.quizId = null;
  builderState.name = "";
  builderState.selectedQuestions = [];
  if (builderElements.nameInput) {
    builderElements.nameInput.value = "";
  }
  if (builderElements.title) {
    builderElements.title.textContent = "New Quiz";
  }
  setFormError("");
  setBuilderError("");
}

async function loadQuizBuilder(quizId = null) {
  resetBuilderState();
  setBuilderLoading(true);
  renderBuilderPanels();

  try {
    builderState.allQuestions = await fetchAllQuestions();

    if (quizId) {
      builderState.mode = "edit";
      builderState.quizId = quizId;
      const quiz = await fetchQuiz(quizId);
      builderState.name = quiz.name;
      builderState.selectedQuestions = quiz.questions ?? [];
      if (builderElements.title) {
        builderElements.title.textContent = "Edit Quiz";
      }
      if (builderElements.nameInput) {
        builderElements.nameInput.value = quiz.name;
      }
    }
  } catch (error) {
    setBuilderError(error instanceof Error ? error.message : "Failed to load quiz builder.");
    console.error(error);
  } finally {
    setBuilderLoading(false);
    renderBuilderPanels();
  }
}

function addQuestionToSelection(questionId) {
  const question = builderState.allQuestions.find((item) => item.id === questionId);
  if (!question || getSelectedQuestionIds().includes(questionId)) {
    return;
  }
  builderState.selectedQuestions.push(question);
  setFormError("");
  renderBuilderPanels();
}

function removeQuestionFromSelection(questionId) {
  builderState.selectedQuestions = builderState.selectedQuestions.filter(
    (question) => question.id !== questionId
  );
  renderBuilderPanels();
}

function moveSelectedQuestion(questionId, direction) {
  const index = builderState.selectedQuestions.findIndex((question) => question.id === questionId);
  if (index === -1) {
    return;
  }

  const targetIndex = direction === "up" ? index - 1 : index + 1;
  if (targetIndex < 0 || targetIndex >= builderState.selectedQuestions.length) {
    return;
  }

  const updated = [...builderState.selectedQuestions];
  const [moved] = updated.splice(index, 1);
  updated.splice(targetIndex, 0, moved);
  builderState.selectedQuestions = updated;
  renderBuilderPanels();
}

function validateBuilderForm() {
  const name = builderElements.nameInput?.value.trim() ?? "";
  if (!name) {
    return "Quiz name is required.";
  }
  if (builderState.selectedQuestions.length < MIN_QUIZ_QUESTIONS) {
    return `A quiz must include at least ${MIN_QUIZ_QUESTIONS} questions.`;
  }
  return "";
}

function buildSavePayload() {
  return {
    name: builderElements.nameInput?.value.trim() ?? "",
    questionIds: getSelectedQuestionIds(),
  };
}

async function handleSaveQuiz() {
  const validationError = validateBuilderForm();
  if (validationError) {
    setFormError(validationError);
    return;
  }

  setFormError("");
  if (builderElements.saveBtn) {
    builderElements.saveBtn.disabled = true;
  }

  try {
    const payload = buildSavePayload();
    if (builderState.mode === "edit" && builderState.quizId !== null) {
      await updateQuiz(builderState.quizId, payload);
    } else {
      await createQuiz(payload);
    }
    window.navigateToPage("quizList");
  } catch (error) {
    setFormError(error instanceof Error ? error.message : "Failed to save quiz.");
    console.error(error);
  } finally {
    if (builderElements.saveBtn) {
      builderElements.saveBtn.disabled = false;
    }
  }
}

function openQuizPreview() {
  if (builderState.selectedQuestions.length === 0) {
    setFormError("Add at least one question to preview the quiz.");
    return;
  }

  if (!builderElements.previewModal || !builderElements.previewContent) {
    return;
  }

  setFormError("");
  const quizName = builderElements.nameInput?.value.trim() || "Untitled Quiz";
  const renderPreview =
    typeof window.renderQuizPreviewContent === "function"
      ? window.renderQuizPreviewContent
      : null;

  if (!renderPreview) {
    setFormError("Preview is unavailable. Reload the page and try again.");
    return;
  }

  builderElements.previewContent.innerHTML = renderPreview(
    quizName,
    builderState.selectedQuestions
  );
  builderElements.previewModal.hidden = false;
}

function closeQuizPreview() {
  if (builderElements.previewModal) {
    builderElements.previewModal.hidden = true;
  }
}

function handleSelectedListClick(event) {
  const actionButton = event.target.closest("[data-action]");
  if (!actionButton) {
    return;
  }

  const row = actionButton.closest("[data-question-id]");
  if (!row) {
    return;
  }

  const questionId = Number(row.dataset.questionId);
  const action = actionButton.dataset.action;

  if (action === "remove") {
    removeQuestionFromSelection(questionId);
  }
  if (action === "up") {
    moveSelectedQuestion(questionId, "up");
  }
  if (action === "down") {
    moveSelectedQuestion(questionId, "down");
  }
}

function handleAvailableListClick(event) {
  const actionButton = event.target.closest("[data-action='add']");
  if (!actionButton) {
    return;
  }

  const row = actionButton.closest("[data-question-id]");
  if (!row) {
    return;
  }

  addQuestionToSelection(Number(row.dataset.questionId));
}

function handlePreviewOverlayClick(event) {
  if (event.target.classList.contains("modal-overlay")) {
    closeQuizPreview();
  }
}

function getBuilderQuizIdFromHash() {
  const hash = window.location.hash.replace(/^#/, "");
  if (hash === "quizCreate") {
    return null;
  }
  const match = hash.match(/^quizCreate\/(\d+)$/);
  return match ? Number(match[1]) : null;
}

function shouldLoadBuilderFromHash() {
  const hash = window.location.hash.replace(/^#/, "");
  return hash === "quizCreate" || /^quizCreate\/\d+$/.test(hash);
}

function initQuizBuilderPage() {
  if (!builderElements.selectedList) {
    return;
  }

  builderElements.backBtn?.addEventListener("click", () => window.navigateToPage("quizList"));
  builderElements.cancelBtn?.addEventListener("click", () => window.navigateToPage("quizList"));
  builderElements.saveBtn?.addEventListener("click", handleSaveQuiz);
  builderElements.previewBtn?.addEventListener("click", openQuizPreview);
  builderElements.selectedList.addEventListener("click", handleSelectedListClick);
  builderElements.availableList?.addEventListener("click", handleAvailableListClick);
  builderElements.previewCloseBtn?.addEventListener("click", closeQuizPreview);
  builderElements.previewDoneBtn?.addEventListener("click", closeQuizPreview);
  builderElements.previewModal?.addEventListener("click", handlePreviewOverlayClick);

  window.refreshQuizBuilder = loadQuizBuilder;
  window.openQuizPreview = openQuizPreview;

  if (shouldLoadBuilderFromHash()) {
    loadQuizBuilder(getBuilderQuizIdFromHash());
  }
}

document.addEventListener("DOMContentLoaded", initQuizBuilderPage);
