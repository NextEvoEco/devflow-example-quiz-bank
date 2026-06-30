const examListState = {
  quizzes: [],
  isLoading: false,
};

const examListElements = {
  listStatus: document.getElementById("exam-list-status"),
  listError: document.getElementById("exam-list-error"),
  examGrid: document.getElementById("exam-grid"),
  emptyState: document.getElementById("exam-empty-state"),
  emptyCreateBtn: document.getElementById("exam-empty-create-btn"),
};

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function getExamDescription(quiz) {
  const count = quiz.questionCount;
  const label = count === 1 ? "question" : "questions";
  return `A ${count}-${label} quiz ready to take as an exam.`;
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

function renderExamCard(quiz) {
  return `
    <article class="exam-card" data-quiz-id="${quiz.id}">
      <div class="exam-card-header">
        <h3>${escapeHtml(quiz.name)}</h3>
        <span class="count-badge">${quiz.questionCount}</span>
      </div>
      <p class="exam-card-description">${escapeHtml(getExamDescription(quiz))}</p>
      <button class="btn btn-primary exam-start-btn" type="button" data-action="start">
        Start Exam
      </button>
    </article>
  `;
}

function renderExamList() {
  if (!examListElements.examGrid || !examListElements.emptyState) {
    return;
  }

  if (examListState.isLoading) {
    examListElements.examGrid.hidden = true;
    examListElements.emptyState.hidden = true;
    return;
  }

  if (examListState.quizzes.length === 0) {
    examListElements.examGrid.hidden = true;
    examListElements.emptyState.hidden = false;
    return;
  }

  examListElements.emptyState.hidden = true;
  examListElements.examGrid.hidden = false;
  examListElements.examGrid.innerHTML = examListState.quizzes
    .map((quiz) => renderExamCard(quiz))
    .join("");
}

function setExamListLoading(isLoading) {
  examListState.isLoading = isLoading;
  if (examListElements.listStatus) {
    examListElements.listStatus.hidden = !isLoading;
  }
}

function setExamListError(message) {
  if (!examListElements.listError) {
    return;
  }
  examListElements.listError.hidden = !message;
  examListElements.listError.textContent = message;
}

async function loadExamList() {
  setExamListError("");
  setExamListLoading(true);
  renderExamList();

  try {
    examListState.quizzes = await fetchQuizzes();
  } catch (error) {
    examListState.quizzes = [];
    setExamListError(error instanceof Error ? error.message : "Failed to load exams.");
    console.error(error);
  } finally {
    setExamListLoading(false);
    renderExamList();
  }
}

function getQuizName(quizId) {
  const quiz = examListState.quizzes.find((item) => item.id === quizId);
  return quiz?.name ?? `Quiz ${quizId}`;
}

function resetExamSession() {
  if (typeof window.abandonExamSession === "function") {
    window.abandonExamSession();
  } else {
    window.examState.currentExamQuizId = null;
    window.examState.examQuestion = 0;
    window.examState.examAnswers = {};
  }
}

function startExam(quizId) {
  resetExamSession();
  window.examState.currentExamQuizId = quizId;
  window.navigateToPage("examTaking", { quizId });
}

function handleExamGridClick(event) {
  const startButton = event.target.closest('[data-action="start"]');
  if (!startButton) {
    return;
  }

  const card = startButton.closest("[data-quiz-id]");
  if (!card) {
    return;
  }

  startExam(Number(card.dataset.quizId));
}

function initExamListPage() {
  if (!examListElements.examGrid) {
    return;
  }

  window.examState = {
    currentExamQuizId: null,
    attemptId: null,
    examQuestion: 0,
    examAnswers: {},
    questions: [],
    quizName: "",
    submitResult: null,
  };

  examListElements.examGrid.addEventListener("click", handleExamGridClick);
  examListElements.emptyCreateBtn?.addEventListener("click", () => {
    window.navigateToPage("quizList");
  });

  window.refreshExamList = loadExamList;
  window.resetExamSession = resetExamSession;
}

document.addEventListener("DOMContentLoaded", initExamListPage);
