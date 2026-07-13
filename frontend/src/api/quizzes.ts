import type { Quiz, QuizSummary } from '../types'

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init)
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.error ?? `Request failed (${response.status})`)
  }
  return response.json()
}

export const fetchQuizzes = () => request<QuizSummary[]>('/api/quizzes')
export const fetchQuiz = (id: number) => request<Quiz>(`/api/quizzes/${id}`)
export const createQuiz = (name: string, questionIds: number[]) =>
  request<Quiz>('/api/quizzes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, question_ids: questionIds }) })
export const updateQuiz = (id: number, name: string, questionIds: number[]) =>
  request<Quiz>(`/api/quizzes/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, question_ids: questionIds }) })
export async function deleteQuiz(id: number) {
  await request(`/api/quizzes/${id}`, { method: 'DELETE' })
}
