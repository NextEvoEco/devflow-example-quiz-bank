const quizListState = {
  quizzes: [],
  isLoading: false,
  deletingQuizId: null,
};

const quizListElements = {
  listStatus: document.getElementById("quiz-list-status"),
  listError: document.getElementById("quiz-list-error"),
  quizGrid: document.getElementById("quiz-grid"),
  emptyState: document.getElementById("quiz-empty-state"),
  createQuizBtn: document.getElementById("create-quiz-btn"),
  emptyCreateQuizBtn: document.getElementById("quiz-empty-create-btn"),
  deleteModal: document.getElementById("quiz-delete-modal"),
  deleteFormError: document.getElementById("quiz-delete-form-error"),
  deleteCancelBtn: document.getElementById("quiz-delete-cancel-btn"),
  deleteConfirmBtn: document.getElementById("quiz-delete-confirm-btn"),
};

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
    throw new Error(message);
  }
  return payload;
}

async function fetchQuizzes() {
  const response = await fetch("/api/quizzes");
  const payload = await parseApiResponse(response);
  return payload.quizzes ?? [];
}

async function deleteQuiz(quizId) {
  const response = await fetch(`/api/quizzes/${quizId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    await parseApiResponse(response);
  }
}

function setQuizListLoading(isLoading) {
  quizListState.isLoading = isLoading;
  if (quizListElements.listStatus) {
    quizListElements.listStatus.hidden = !isLoading;
  }
}

function setQuizListError(message) {
  if (!quizListElements.listError) {
    return;
  }
  quizListElements.listError.hidden = !message;
  quizListElements.listError.textContent = message;
}

function renderQuizCard(quiz) {
  return `
    <article class="quiz-card" data-quiz-id="${quiz.id}">
      <div class="quiz-card-header">
        <h3>${escapeHtml(quiz.name)}</h3>
        <span class="count-badge">${quiz.questionCount}</span>
      </div>
      <div class="quiz-card-actions">
        <button class="btn btn-secondary btn-compact" type="button" data-action="edit">Edit</button>
        <button class="btn btn-danger btn-compact" type="button" data-action="delete">Delete</button>
      </div>
    </article>
  `;
}

function renderQuizList() {
  if (!quizListElements.quizGrid || !quizListElements.emptyState) {
    return;
  }

  if (quizListState.isLoading) {
    quizListElements.quizGrid.hidden = true;
    quizListElements.emptyState.hidden = true;
    return;
  }

  if (quizListState.quizzes.length === 0) {
    quizListElements.quizGrid.hidden = true;
    quizListElements.emptyState.hidden = false;
    return;
  }

  quizListElements.emptyState.hidden = true;
  quizListElements.quizGrid.hidden = false;
  quizListElements.quizGrid.innerHTML = quizListState.quizzes
    .map((quiz) => renderQuizCard(quiz))
    .join("");
}

async function loadQuizzes() {
  setQuizListError("");
  setQuizListLoading(true);
  renderQuizList();

  try {
    quizListState.quizzes = await fetchQuizzes();
  } catch (error) {
    quizListState.quizzes = [];
    setQuizListError(error instanceof Error ? error.message : "Failed to load quizzes.");
    console.error(error);
  } finally {
    setQuizListLoading(false);
    renderQuizList();
  }
}

function openQuizDeleteModal(quizId) {
  quizListState.deletingQuizId = quizId;
  if (quizListElements.deleteFormError) {
    quizListElements.deleteFormError.hidden = true;
    quizListElements.deleteFormError.textContent = "";
  }
  if (quizListElements.deleteModal) {
    quizListElements.deleteModal.hidden = false;
  }
}

function closeQuizDeleteModal() {
  quizListState.deletingQuizId = null;
  if (quizListElements.deleteModal) {
    quizListElements.deleteModal.hidden = true;
  }
}

async function handleConfirmQuizDelete() {
  if (quizListState.deletingQuizId === null) {
    return;
  }

  if (quizListElements.deleteFormError) {
    quizListElements.deleteFormError.hidden = true;
  }
  if (quizListElements.deleteConfirmBtn) {
    quizListElements.deleteConfirmBtn.disabled = true;
  }

  try {
    await deleteQuiz(quizListState.deletingQuizId);
    closeQuizDeleteModal();
    await loadQuizzes();
  } catch (error) {
    if (quizListElements.deleteFormError) {
      quizListElements.deleteFormError.hidden = false;
      quizListElements.deleteFormError.textContent =
        error instanceof Error ? error.message : "Failed to delete quiz.";
    }
    console.error(error);
  } finally {
    if (quizListElements.deleteConfirmBtn) {
      quizListElements.deleteConfirmBtn.disabled = false;
    }
  }
}

function handleQuizGridClick(event) {
  const actionButton = event.target.closest("[data-action]");
  if (!actionButton) {
    return;
  }

  const card = actionButton.closest("[data-quiz-id]");
  if (!card) {
    return;
  }

  const quizId = Number(card.dataset.quizId);

  if (actionButton.dataset.action === "edit") {
    window.navigateToPage("quizCreate", { quizId });
  }

  if (actionButton.dataset.action === "delete") {
    openQuizDeleteModal(quizId);
  }
}

function handleQuizDeleteOverlayClick(event) {
  if (event.target.classList.contains("modal-overlay")) {
    closeQuizDeleteModal();
  }
}

function initQuizListPage() {
  if (!quizListElements.quizGrid) {
    return;
  }

  quizListElements.createQuizBtn?.addEventListener("click", () => {
    window.navigateToPage("quizCreate");
  });
  quizListElements.emptyCreateQuizBtn?.addEventListener("click", () => {
    window.navigateToPage("quizCreate");
  });
  quizListElements.quizGrid.addEventListener("click", handleQuizGridClick);

  quizListElements.deleteCancelBtn?.addEventListener("click", closeQuizDeleteModal);
  quizListElements.deleteConfirmBtn?.addEventListener("click", handleConfirmQuizDelete);
  quizListElements.deleteModal?.addEventListener("click", handleQuizDeleteOverlayClick);

  window.refreshQuizList = loadQuizzes;
}

document.addEventListener("DOMContentLoaded", initQuizListPage);
