const SCORE_RING_RADIUS = 54;
const SCORE_RING_CIRCUMFERENCE = 2 * Math.PI * SCORE_RING_RADIUS;

const examResultsElements = {
  quizLabel: document.getElementById("exam-results-quiz-label"),
  scoreRingProgress: document.getElementById("exam-score-ring-progress"),
  scorePercentage: document.getElementById("exam-score-percentage"),
  scoreFraction: document.getElementById("exam-score-fraction"),
  correctCount: document.getElementById("exam-correct-count"),
  incorrectCount: document.getElementById("exam-incorrect-count"),
  answerReviewList: document.getElementById("exam-answer-review-list"),
  backBtn: document.getElementById("exam-back-to-list-btn"),
  retryBtn: document.getElementById("exam-retry-btn"),
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function getExamState() {
  return window.examState;
}

function getScoreRingColor(percentage) {
  if (percentage >= 70) {
    return "#15803d";
  }
  if (percentage >= 50) {
    return "#b45309";
  }
  return "#b91c1c";
}

function formatAnswerLabel(optionKey, answer) {
  if (!optionKey) {
    return "No answer";
  }
  const optionText = answer[optionKey.toLowerCase()];
  return `${optionKey}: ${optionText}`;
}

function renderAnswerReviewItem(answer) {
  const statusClass = answer.is_correct ? "is-correct" : "is-incorrect";
  const statusIcon = answer.is_correct ? "✓" : "✗";
  const statusLabel = answer.is_correct ? "Correct" : "Incorrect";
  const userAnswer = formatAnswerLabel(answer.selected_option, answer);
  const correctAnswer = formatAnswerLabel(answer.correct_option, answer);
  const correctAnswerLine = answer.is_correct
    ? ""
    : `<p class="exam-review-correct">Correct: ${escapeHtml(correctAnswer)}</p>`;

  return `
    <article class="exam-review-item ${statusClass}">
      <div class="exam-review-status" aria-hidden="true">${statusIcon}</div>
      <div class="exam-review-content">
        <p class="exam-review-question">${escapeHtml(answer.question_text)}</p>
        <p class="exam-review-user">Your answer: ${escapeHtml(userAnswer)}</p>
        ${correctAnswerLine}
        <span class="exam-review-badge">${statusLabel}</span>
      </div>
    </article>
  `;
}

function renderScoreSummary(result) {
  const percentage = result.percentage ?? 0;
  const score = result.score ?? 0;
  const total = result.total ?? 0;
  const incorrectCount = total - score;
  const ringColor = getScoreRingColor(percentage);
  const dashOffset = SCORE_RING_CIRCUMFERENCE * (1 - percentage / 100);

  if (examResultsElements.scorePercentage) {
    examResultsElements.scorePercentage.textContent = `${percentage}%`;
  }
  if (examResultsElements.scoreFraction) {
    examResultsElements.scoreFraction.textContent = `${score} / ${total}`;
  }
  if (examResultsElements.scoreRingProgress) {
    examResultsElements.scoreRingProgress.style.stroke = ringColor;
    examResultsElements.scoreRingProgress.style.strokeDasharray = `${SCORE_RING_CIRCUMFERENCE}`;
    examResultsElements.scoreRingProgress.style.strokeDashoffset = `${dashOffset}`;
  }
  if (examResultsElements.correctCount) {
    examResultsElements.correctCount.innerHTML = `
      <span class="exam-score-count-value">${score}</span>
      <span class="exam-score-count-label">Correct</span>
    `;
  }
  if (examResultsElements.incorrectCount) {
    examResultsElements.incorrectCount.innerHTML = `
      <span class="exam-score-count-value">${incorrectCount}</span>
      <span class="exam-score-count-label">Incorrect</span>
    `;
  }
}

function renderAnswerReview(result) {
  if (!examResultsElements.answerReviewList) {
    return;
  }

  const answers = result.answers ?? [];
  examResultsElements.answerReviewList.innerHTML = answers
    .map((answer) => renderAnswerReviewItem(answer))
    .join("");
}

function clearExamResultsSession() {
  const state = getExamState();
  state.submitResult = null;
  state.currentExamQuizId = null;
  state.attemptId = null;
  state.examQuestion = 0;
  state.examAnswers = {};
  state.questions = [];
  state.quizName = "";
}

function refreshExamResults() {
  const state = getExamState();
  if (!state.submitResult) {
    window.navigateToPage("examList");
    return;
  }

  if (examResultsElements.quizLabel) {
    examResultsElements.quizLabel.textContent = state.quizName;
  }

  renderScoreSummary(state.submitResult);
  renderAnswerReview(state.submitResult);
}

function handleBackToExams() {
  clearExamResultsSession();
  window.navigateToPage("examList");
}

function handleRetryQuiz() {
  const state = getExamState();
  const quizId = state.currentExamQuizId;
  if (!quizId) {
    window.navigateToPage("examList");
    return;
  }

  state.submitResult = null;
  state.attemptId = null;
  state.examQuestion = 0;
  state.examAnswers = {};
  state.questions = [];
  window.navigateToPage("examTaking", { quizId });
}

function initExamResultsPage() {
  if (!examResultsElements.answerReviewList) {
    return;
  }

  if (examResultsElements.scoreRingProgress) {
    examResultsElements.scoreRingProgress.style.strokeDasharray = `${SCORE_RING_CIRCUMFERENCE}`;
    examResultsElements.scoreRingProgress.style.strokeDashoffset = `${SCORE_RING_CIRCUMFERENCE}`;
  }

  examResultsElements.backBtn?.addEventListener("click", handleBackToExams);
  examResultsElements.retryBtn?.addEventListener("click", handleRetryQuiz);

  window.refreshExamResults = refreshExamResults;
  window.clearExamResultsSession = clearExamResultsSession;
}

document.addEventListener("DOMContentLoaded", initExamResultsPage);
