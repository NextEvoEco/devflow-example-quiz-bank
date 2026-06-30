const OPTION_KEYS = ["A", "B", "C", "D"];

const examTakingElements = {
  quizLabel: document.getElementById("exam-taking-quiz-label"),
  progressLabel: document.getElementById("exam-taking-progress-label"),
  progressFill: document.getElementById("exam-progress-fill"),
  questionJump: document.getElementById("exam-question-jump"),
  status: document.getElementById("exam-taking-status"),
  error: document.getElementById("exam-taking-error"),
  questionCard: document.getElementById("exam-question-card"),
  questionText: document.getElementById("exam-question-text"),
  optionList: document.getElementById("exam-option-list"),
  prevBtn: document.getElementById("exam-prev-btn"),
  nextBtn: document.getElementById("exam-next-btn"),
  exitBtn: document.getElementById("exam-exit-btn"),
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
  if (response.status === 204) {
    if (!response.ok) {
      throw new Error(`Request failed (${response.status})`);
    }
    return null;
  }

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = payload.error || `Request failed (${response.status})`;
    throw new Error(message);
  }
  return payload;
}

async function fetchQuizDetail(quizId) {
  const response = await fetch(`/api/quizzes/${quizId}`);
  return parseApiResponse(response);
}

async function createExamAttempt(quizId) {
  const response = await fetch("/api/exams/attempts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ quiz_id: quizId }),
  });
  return parseApiResponse(response);
}

async function saveExamAnswer(attemptId, questionId, selectedOption) {
  const response = await fetch(
    `/api/exams/attempts/${attemptId}/answers/${questionId}`,
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selected_option: selectedOption }),
    }
  );
  await parseApiResponse(response);
}

async function submitExamAttempt(attemptId) {
  const response = await fetch(`/api/exams/attempts/${attemptId}/submit`, {
    method: "POST",
  });
  return parseApiResponse(response);
}

function getExamState() {
  return window.examState;
}

function setExamTakingLoading(isLoading) {
  if (examTakingElements.status) {
    examTakingElements.status.hidden = !isLoading;
  }
}

function setExamTakingError(message) {
  if (!examTakingElements.error) {
    return;
  }
  examTakingElements.error.hidden = !message;
  examTakingElements.error.textContent = message;
}

function getCurrentQuestion() {
  const state = getExamState();
  return state.questions[state.examQuestion] ?? null;
}

function renderQuestionJumpButtons() {
  const state = getExamState();
  if (!examTakingElements.questionJump) {
    return;
  }

  examTakingElements.questionJump.innerHTML = state.questions
    .map((_, index) => {
      const isActive = index === state.examQuestion;
      const isAnswered = state.examAnswers[state.questions[index].id] !== undefined;
      const classes = ["exam-jump-btn"];
      if (isActive) {
        classes.push("is-active");
      }
      if (isAnswered) {
        classes.push("is-answered");
      }
      return `<button type="button" class="${classes.join(" ")}" data-question-index="${index}">${index + 1}</button>`;
    })
    .join("");
}

function renderExamProgress() {
  const state = getExamState();
  const total = state.questions.length;
  const current = total ? state.examQuestion + 1 : 0;

  if (examTakingElements.progressLabel) {
    examTakingElements.progressLabel.textContent = `Question ${current} of ${total}`;
  }
  if (examTakingElements.progressFill && total) {
    examTakingElements.progressFill.style.width = `${(current / total) * 100}%`;
  }
  if (examTakingElements.quizLabel) {
    examTakingElements.quizLabel.textContent = state.quizName;
  }
}

function renderOptionButton(optionKey, optionText, isSelected) {
  const selectedClass = isSelected ? " is-selected" : "";
  return `
    <button
      type="button"
      class="exam-option-btn${selectedClass}"
      data-option="${optionKey}"
    >
      <span class="exam-option-label">${optionKey}</span>
      <span class="exam-option-text">${escapeHtml(optionText)}</span>
      <span class="exam-option-check" aria-hidden="true">✓</span>
    </button>
  `;
}

function renderExamQuestion() {
  const state = getExamState();
  const question = getCurrentQuestion();

  if (!question || !examTakingElements.questionCard) {
    return;
  }

  const selectedOption = state.examAnswers[question.id] ?? null;

  examTakingElements.questionText.textContent = question.question;
  examTakingElements.optionList.innerHTML = OPTION_KEYS.map((optionKey) =>
    renderOptionButton(
      optionKey,
      question[optionKey.toLowerCase()],
      selectedOption === optionKey
    )
  ).join("");

  renderExamProgress();
  renderQuestionJumpButtons();

  if (examTakingElements.prevBtn) {
    examTakingElements.prevBtn.disabled = state.examQuestion === 0;
    examTakingElements.prevBtn.classList.toggle("is-dimmed", state.examQuestion === 0);
  }

  const isLastQuestion = state.examQuestion === state.questions.length - 1;
  if (examTakingElements.nextBtn) {
    examTakingElements.nextBtn.textContent = isLastQuestion ? "Submit" : "Next";
  }

  examTakingElements.questionCard.hidden = false;
}

async function initializeExamSession(quizId) {
  const state = getExamState();
  setExamTakingError("");
  setExamTakingLoading(true);
  examTakingElements.questionCard.hidden = true;

  try {
    const quiz = await fetchQuizDetail(quizId);
    const attempt = await createExamAttempt(quizId);

    state.currentExamQuizId = quizId;
    state.attemptId = attempt.attempt_id;
    state.quizName = quiz.name;
    state.questions = quiz.questions ?? [];
    state.examQuestion = 0;
    state.examAnswers = {};
    state.submitResult = null;
  } catch (error) {
    setExamTakingError(error instanceof Error ? error.message : "Failed to start exam.");
    console.error(error);
    throw error;
  } finally {
    setExamTakingLoading(false);
  }
}

async function refreshExamTaking(quizId) {
  if (!quizId) {
    return;
  }

  const state = getExamState();
  const hasActiveSession =
    state.currentExamQuizId === quizId &&
    state.attemptId !== null &&
    state.questions.length > 0;

  try {
    if (!hasActiveSession) {
      await initializeExamSession(quizId);
    }
    renderExamQuestion();
  } catch {
    // Error message already shown.
  }
}

function abandonExamSession() {
  const state = getExamState();
  state.currentExamQuizId = null;
  state.attemptId = null;
  state.examQuestion = 0;
  state.examAnswers = {};
  state.questions = [];
  state.quizName = "";
  state.submitResult = null;
}

function goToQuestion(index) {
  const state = getExamState();
  if (index < 0 || index >= state.questions.length) {
    return;
  }
  state.examQuestion = index;
  renderExamQuestion();
}

async function handleOptionSelect(optionKey) {
  const state = getExamState();
  const question = getCurrentQuestion();
  if (!question || !state.attemptId) {
    return;
  }

  state.examAnswers[question.id] = optionKey;
  renderExamQuestion();

  try {
    await saveExamAnswer(state.attemptId, question.id, optionKey);
  } catch (error) {
    setExamTakingError(error instanceof Error ? error.message : "Failed to save answer.");
    console.error(error);
  }
}

async function handleSubmitExam() {
  const state = getExamState();
  if (!state.attemptId) {
    return;
  }

  setExamTakingError("");
  if (examTakingElements.nextBtn) {
    examTakingElements.nextBtn.disabled = true;
  }

  try {
    const result = await submitExamAttempt(state.attemptId);
    state.submitResult = result;
    state.attemptId = null;
    window.navigateToPage("examResults");
  } catch (error) {
    setExamTakingError(error instanceof Error ? error.message : "Failed to submit exam.");
    console.error(error);
  } finally {
    if (examTakingElements.nextBtn) {
      examTakingElements.nextBtn.disabled = false;
    }
  }
}

function handleNextClick() {
  const state = getExamState();
  const isLastQuestion = state.examQuestion === state.questions.length - 1;
  if (isLastQuestion) {
    handleSubmitExam();
    return;
  }
  goToQuestion(state.examQuestion + 1);
}

function handlePreviousClick() {
  const state = getExamState();
  if (state.examQuestion === 0) {
    return;
  }
  goToQuestion(state.examQuestion - 1);
}

function handleQuestionJumpClick(event) {
  const button = event.target.closest("[data-question-index]");
  if (!button) {
    return;
  }
  goToQuestion(Number(button.dataset.questionIndex));
}

function handleOptionListClick(event) {
  const optionButton = event.target.closest("[data-option]");
  if (!optionButton) {
    return;
  }
  handleOptionSelect(optionButton.dataset.option);
}

function initExamTakingPage() {
  if (!examTakingElements.questionCard) {
    return;
  }

  examTakingElements.optionList?.addEventListener("click", handleOptionListClick);
  examTakingElements.questionJump?.addEventListener("click", handleQuestionJumpClick);
  examTakingElements.prevBtn?.addEventListener("click", handlePreviousClick);
  examTakingElements.nextBtn?.addEventListener("click", handleNextClick);
  examTakingElements.exitBtn?.addEventListener("click", () => {
    abandonExamSession();
    window.navigateToPage("examList");
  });

  window.refreshExamTaking = refreshExamTaking;
  window.abandonExamSession = abandonExamSession;
}

document.addEventListener("DOMContentLoaded", initExamTakingPage);
