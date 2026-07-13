import type { Question, QuestionInput, QuizDetail, QuizInput, QuizSummary } from './types'

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })
  if (response.status === 204) {
    return undefined as T
  }
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const message =
      typeof data?.error === 'string' ? data.error : `Request failed (${response.status})`
    throw new Error(message)
  }
  return data as T
}

export function listQuestions(search = ''): Promise<Question[]> {
  const query = search.trim() ? `?q=${encodeURIComponent(search.trim())}` : ''
  return request<Question[]>(`/api/questions${query}`)
}

export function createQuestion(payload: QuestionInput): Promise<Question> {
  return request<Question>('/api/questions', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateQuestion(id: number, payload: QuestionInput): Promise<Question> {
  return request<Question>(`/api/questions/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteQuestion(id: number): Promise<void> {
  return request<void>(`/api/questions/${id}`, { method: 'DELETE' })
}

export function listQuizzes(): Promise<QuizSummary[]> {
  return request<QuizSummary[]>('/api/quizzes')
}

export function getQuiz(id: number): Promise<QuizDetail> {
  return request<QuizDetail>(`/api/quizzes/${id}`)
}

export function createQuiz(payload: QuizInput): Promise<QuizDetail> {
  return request<QuizDetail>('/api/quizzes', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateQuiz(id: number, payload: QuizInput): Promise<QuizDetail> {
  return request<QuizDetail>(`/api/quizzes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteQuiz(id: number): Promise<void> {
  return request<void>(`/api/quizzes/${id}`, { method: 'DELETE' })
}

export interface ExamSubmitResult {
  attempt_id: number
  quiz_id: number
  quiz_name: string
  score: number
  total: number
  percentage: number
  answers: Array<{
    question_id: number
    question_text: string
    selected_option: string | null
    selected_text: string | null
    correct_option: string
    correct_text: string
    is_correct: boolean
  }>
}

export function startExamAttempt(quizId: number): Promise<{ attempt_id: number; quiz_id: number }> {
  return request('/api/exams/attempts', {
    method: 'POST',
    body: JSON.stringify({ quiz_id: quizId }),
  })
}

export function saveExamAnswer(
  attemptId: number,
  questionId: number,
  selectedOption: string,
): Promise<void> {
  return request(`/api/exams/attempts/${attemptId}/answers/${questionId}`, {
    method: 'PUT',
    body: JSON.stringify({ selected_option: selectedOption }),
  })
}

export function submitExamAttempt(attemptId: number): Promise<ExamSubmitResult> {
  return request(`/api/exams/attempts/${attemptId}/submit`, { method: 'POST' })
}
