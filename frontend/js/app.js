const state = {
  questions: [],
  searchQuery: "",
  isLoading: false,
  errorMessage: "",
  editorMode: "add",
  editingQuestionId: null,
  deletingQuestionId: null,
};

const elements = {
  countBadge: document.getElementById("question-count"),
  searchInput: document.getElementById("search-input"),
  listStatus: document.getElementById("question-list-status"),
  listError: document.getElementById("question-list-error"),
  questionTable: document.getElementById("question-table"),
  questionTableBody: document.getElementById("question-table-body"),
  emptyState: document.getElementById("empty-state"),
  emptyStateMessage: document.getElementById("empty-state-message"),
  addQuestionBtn: document.getElementById("add-question-btn"),
  emptyAddQuestionBtn: document.getElementById("empty-add-question-btn"),
  editorModal: document.getElementById("editor-modal"),
  editorModalTitle: document.getElementById("editor-modal-title"),
  editorForm: document.getElementById("question-form"),
  editorFormError: document.getElementById("editor-form-error"),
  editorCloseBtn: document.getElementById("editor-close-btn"),
  editorCancelBtn: document.getElementById("editor-cancel-btn"),
  editorSaveBtn: document.getElementById("editor-save-btn"),
  deleteModal: document.getElementById("delete-modal"),
  deleteFormError: document.getElementById("delete-form-error"),
  deleteCancelBtn: document.getElementById("delete-cancel-btn"),
  deleteConfirmBtn: document.getElementById("delete-confirm-btn"),
  fieldQuestion: document.getElementById("field-question"),
  fieldA: document.getElementById("field-a"),
  fieldB: document.getElementById("field-b"),
  fieldC: document.getElementById("field-c"),
  fieldD: document.getElementById("field-d"),
  fieldCorrect: document.getElementById("field-correct"),
  fieldDifficulty: document.getElementById("field-difficulty"),
};

function difficultyClass(difficulty) {
  return `difficulty-badge difficulty-${difficulty.toLowerCase()}`;
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function parseApiResponse(response) {
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = payload.error || `Request failed (${response.status})`;
    const error = new Error(message);
    error.field = payload.field ?? null;
    throw error;
  }
  return payload;
}

async function fetchQuestions(searchQuery = "") {
  const trimmedQuery = searchQuery.trim();
  const url = trimmedQuery
    ? `/api/questions?q=${encodeURIComponent(trimmedQuery)}`
    : "/api/questions";

  const response = await fetch(url);
  const payload = await parseApiResponse(response);
  return payload.questions ?? [];
}

async function createQuestion(payload) {
  const response = await fetch("/api/questions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseApiResponse(response);
}

async function updateQuestion(questionId, payload) {
  const response = await fetch(`/api/questions/${questionId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseApiResponse(response);
}

async function deleteQuestion(questionId) {
  const response = await fetch(`/api/questions/${questionId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    await parseApiResponse(response);
  }
}

function getQuestionById(questionId) {
  return state.questions.find((question) => question.id === questionId) ?? null;
}

function renderQuestionRow(question) {
  return `
    <tr data-question-id="${question.id}">
      <td class="question-text">${escapeHtml(question.question)}</td>
      <td class="col-difficulty">
        <span class="${difficultyClass(question.difficulty)}">${escapeHtml(question.difficulty)}</span>
      </td>
      <td class="col-actions">
        <div class="row-actions">
          <button class="btn btn-secondary btn-compact" type="button" data-action="edit">Edit</button>
          <button class="btn btn-danger btn-compact" type="button" data-action="delete">Del</button>
        </div>
      </td>
    </tr>
  `;
}

function setLoading(isLoading) {
  state.isLoading = isLoading;
  elements.listStatus.hidden = !isLoading;
}

function setError(message) {
  state.errorMessage = message;
  elements.listError.hidden = !message;
  elements.listError.textContent = message;
}

function setEditorError(message) {
  elements.editorFormError.hidden = !message;
  elements.editorFormError.textContent = message;
}

function setDeleteError(message) {
  elements.deleteFormError.hidden = !message;
  elements.deleteFormError.textContent = message;
}

function renderQuestionList() {
  const questionCount = state.questions.length;
  elements.countBadge.textContent = String(questionCount);

  if (state.isLoading) {
    elements.questionTable.hidden = true;
    elements.emptyState.hidden = true;
    return;
  }

  if (questionCount === 0) {
    elements.questionTable.hidden = true;
    elements.emptyState.hidden = false;
    elements.emptyStateMessage.textContent = state.searchQuery.trim()
      ? "No questions match your search."
      : "Your question bank is empty. Add a question to get started.";
    return;
  }

  elements.emptyState.hidden = true;
  elements.questionTable.hidden = false;
  elements.questionTableBody.innerHTML = state.questions
    .map((question) => renderQuestionRow(question))
    .join("");
}

async function loadQuestions() {
  setError("");
  setLoading(true);
  renderQuestionList();

  try {
    state.questions = await fetchQuestions(state.searchQuery);
  } catch (error) {
    state.questions = [];
    setError(error instanceof Error ? error.message : "Failed to load questions.");
    console.error(error);
  } finally {
    setLoading(false);
    renderQuestionList();
  }
}

function getFormPayload() {
  return {
    question: elements.fieldQuestion.value,
    a: elements.fieldA.value,
    b: elements.fieldB.value,
    c: elements.fieldC.value,
    d: elements.fieldD.value,
    correct: elements.fieldCorrect.value,
    difficulty: elements.fieldDifficulty.value,
  };
}

function resetEditorForm() {
  elements.editorForm.reset();
  elements.fieldCorrect.value = "A";
  elements.fieldDifficulty.value = "Medium";
  setEditorError("");
}

function fillEditorForm(question) {
  elements.fieldQuestion.value = question.question;
  elements.fieldA.value = question.a;
  elements.fieldB.value = question.b;
  elements.fieldC.value = question.c;
  elements.fieldD.value = question.d;
  elements.fieldCorrect.value = question.correct;
  elements.fieldDifficulty.value = question.difficulty;
  setEditorError("");
}

function validateFormClient(payload) {
  if (!payload.question.trim()) {
    return { message: "Question text is required.", field: "question" };
  }
  for (const field of ["a", "b", "c", "d"]) {
    if (!payload[field].trim()) {
      return { message: `Option ${field.toUpperCase()} is required.`, field };
    }
  }
  return null;
}

function openEditorModal(mode, question = null) {
  state.editorMode = mode;
  state.editingQuestionId = question?.id ?? null;
  elements.editorModalTitle.textContent =
    mode === "edit" ? "Edit Question" : "Add Question";

  if (mode === "edit" && question) {
    fillEditorForm(question);
  } else {
    resetEditorForm();
  }

  elements.editorModal.hidden = false;
  elements.fieldQuestion.focus();
}

function closeEditorModal() {
  elements.editorModal.hidden = true;
  state.editorMode = "add";
  state.editingQuestionId = null;
  resetEditorForm();
}

function openDeleteModal(questionId) {
  state.deletingQuestionId = questionId;
  setDeleteError("");
  elements.deleteModal.hidden = false;
}

function closeDeleteModal() {
  elements.deleteModal.hidden = true;
  state.deletingQuestionId = null;
  setDeleteError("");
}

async function handleSaveQuestion() {
  const payload = getFormPayload();
  const clientError = validateFormClient(payload);
  if (clientError) {
    setEditorError(clientError.message);
    return;
  }

  setEditorError("");
  elements.editorSaveBtn.disabled = true;

  try {
    if (state.editorMode === "edit" && state.editingQuestionId !== null) {
      await updateQuestion(state.editingQuestionId, payload);
    } else {
      await createQuestion(payload);
    }
    closeEditorModal();
    await loadQuestions();
  } catch (error) {
    setEditorError(error instanceof Error ? error.message : "Failed to save question.");
    console.error(error);
  } finally {
    elements.editorSaveBtn.disabled = false;
  }
}

async function handleConfirmDelete() {
  if (state.deletingQuestionId === null) {
    return;
  }

  setDeleteError("");
  elements.deleteConfirmBtn.disabled = true;

  try {
    await deleteQuestion(state.deletingQuestionId);
    closeDeleteModal();
    await loadQuestions();
  } catch (error) {
    setDeleteError(error instanceof Error ? error.message : "Failed to delete question.");
    console.error(error);
  } finally {
    elements.deleteConfirmBtn.disabled = false;
  }
}

function handleSearchInput(event) {
  state.searchQuery = event.target.value;
  loadQuestions();
}

function handleTableClick(event) {
  const actionButton = event.target.closest("[data-action]");
  if (!actionButton) {
    return;
  }

  const row = actionButton.closest("[data-question-id]");
  if (!row) {
    return;
  }

  const questionId = Number(row.dataset.questionId);
  const question = getQuestionById(questionId);
  if (!question) {
    return;
  }

  if (actionButton.dataset.action === "edit") {
    openEditorModal("edit", question);
  }

  if (actionButton.dataset.action === "delete") {
    openDeleteModal(questionId);
  }
}

function handleOverlayClick(event, closeModal) {
  if (event.target.classList.contains("modal-overlay")) {
    closeModal();
  }
}

function initQuestionBankPage() {
  if (!elements.searchInput) {
    return;
  }

  elements.searchInput.addEventListener("input", handleSearchInput);
  elements.addQuestionBtn.addEventListener("click", () => openEditorModal("add"));
  elements.emptyAddQuestionBtn.addEventListener("click", () => openEditorModal("add"));
  elements.questionTableBody.addEventListener("click", handleTableClick);

  elements.editorCloseBtn.addEventListener("click", closeEditorModal);
  elements.editorCancelBtn.addEventListener("click", closeEditorModal);
  elements.editorSaveBtn.addEventListener("click", handleSaveQuestion);
  elements.editorModal.addEventListener("click", (event) =>
    handleOverlayClick(event, closeEditorModal)
  );
  elements.editorForm.addEventListener("submit", (event) => {
    event.preventDefault();
    handleSaveQuestion();
  });

  elements.deleteCancelBtn.addEventListener("click", closeDeleteModal);
  elements.deleteConfirmBtn.addEventListener("click", handleConfirmDelete);
  elements.deleteModal.addEventListener("click", (event) =>
    handleOverlayClick(event, closeDeleteModal)
  );

  loadQuestions();
}

window.refreshQuestionBank = loadQuestions;

document.addEventListener("DOMContentLoaded", initQuestionBankPage);
