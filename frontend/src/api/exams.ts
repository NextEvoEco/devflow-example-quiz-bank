import type { CorrectOption, ExamResult } from '../types'

async function check(response: Response) {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.error ?? `Request failed (${response.status})`)
  }
  return response
}

export async function startAttempt(quizId: number): Promise<number> {
  const response = await check(await fetch('/api/exams/attempts', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ quiz_id: quizId }),
  }))
  return (await response.json()).attempt_id
}
export async function saveAnswer(attemptId: number, questionId: number, selectedOption: CorrectOption) {
  await check(await fetch(`/api/exams/attempts/${attemptId}/answers/${questionId}`, {
    method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ selected_option: selectedOption }),
  }))
}
export async function submitAttempt(attemptId: number): Promise<ExamResult> {
  const response = await check(await fetch(`/api/exams/attempts/${attemptId}/submit`, { method: 'POST' }))
  return response.json()
}
