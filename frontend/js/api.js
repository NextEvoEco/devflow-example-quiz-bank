async function parseJsonResponse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(data.error || "Request failed.");
    error.status = response.status;
    error.errors = data.errors || {};
    throw error;
  }
  return data;
}

async function sendJson(url, method, payload) {
  const response = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseJsonResponse(response);
}

export async function fetchQuestions(query = "") {
  const url = query ? `/api/questions?q=${encodeURIComponent(query)}` : "/api/questions";
  const data = await parseJsonResponse(await fetch(url));
  return data.questions ?? [];
}

export async function getQuestion(questionId) {
  const data = await parseJsonResponse(await fetch(`/api/questions/${questionId}`));
  return data.question;
}

export async function createQuestion(payload) {
  const data = await sendJson("/api/questions", "POST", payload);
  return data.question;
}

export async function updateQuestion(questionId, payload) {
  const data = await sendJson(`/api/questions/${questionId}`, "PUT", payload);
  return data.question;
}

export async function deleteQuestion(questionId) {
  const response = await fetch(`/api/questions/${questionId}`, { method: "DELETE" });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    const error = new Error(data.error || "Failed to delete question.");
    error.status = response.status;
    throw error;
  }
}

export async function fetchQuizzes() {
  const data = await parseJsonResponse(await fetch("/api/quizzes"));
  return data.quizzes ?? [];
}

export async function deleteQuiz(quizId) {
  const response = await fetch(`/api/quizzes/${quizId}`, { method: "DELETE" });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    const error = new Error(data.error || "Failed to delete quiz.");
    error.status = response.status;
    throw error;
  }
}

export async function getQuiz(quizId) {
  const data = await parseJsonResponse(await fetch(`/api/quizzes/${quizId}`));
  return data.quiz;
}

export async function createQuiz(payload) {
  const data = await sendJson("/api/quizzes", "POST", payload);
  return data.quiz;
}

export async function updateQuiz(quizId, payload) {
  const data = await sendJson(`/api/quizzes/${quizId}`, "PUT", payload);
  return data.quiz;
}

export async function createExamAttempt(quizId) {
  const data = await sendJson("/api/exams/attempts", "POST", { quiz_id: quizId });
  return data.attempt_id;
}

export async function saveExamAnswer(attemptId, questionId, selectedOption) {
  const response = await fetch(
    `/api/exams/attempts/${attemptId}/answers/${questionId}`,
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selected_option: selectedOption }),
    },
  );
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    const error = new Error(data.error || "Failed to save answer.");
    error.status = response.status;
    throw error;
  }
}

export async function submitExamAttempt(attemptId) {
  return sendJson(`/api/exams/attempts/${attemptId}/submit`, "POST", {});
}
