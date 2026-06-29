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

function renderPreviewOption(label, text, isCorrect) {
  return `
    <li class="preview-option ${isCorrect ? "is-correct" : ""}">
      <span class="preview-option-label">${label}.</span>
      <span class="preview-option-text">${escapeHtml(text)}</span>
      ${isCorrect ? '<span class="preview-correct-label">Correct answer</span>' : ""}
    </li>
  `;
}

function renderPreviewQuestion(question, index) {
  const options = [
    ["A", question.a],
    ["B", question.b],
    ["C", question.c],
    ["D", question.d],
  ];

  const optionsHtml = options
    .map(([label, text]) => renderPreviewOption(label, text, label === question.correct))
    .join("");

  return `
    <article class="preview-question-card">
      <header class="preview-question-header">
        <h3>Question ${index + 1}</h3>
        <span class="${difficultyClass(question.difficulty)}">${escapeHtml(question.difficulty)}</span>
      </header>
      <p class="preview-question-text">${escapeHtml(question.question)}</p>
      <ul class="preview-options" aria-label="Answer options for question ${index + 1}">
        ${optionsHtml}
      </ul>
    </article>
  `;
}

function renderQuizPreviewContent(quizName, questions) {
  const safeName = quizName.trim() || "Untitled Quiz";
  const questionLabel = questions.length === 1 ? "question" : "questions";
  const questionsHtml = questions
    .map((question, index) => renderPreviewQuestion(question, index))
    .join("");

  return `
    <p class="preview-quiz-name">${escapeHtml(safeName)}</p>
    <p class="preview-meta">${questions.length} ${questionLabel}</p>
    ${questionsHtml}
  `;
}

window.renderQuizPreviewContent = renderQuizPreviewContent;
