import type { Question, QuestionInput } from '../types'

async function parseError(response: Response): Promise<string> {
  try {
    const body = await response.json()
    if (typeof body.error === 'string') {
      return body.error
    }
  } catch {
    // ignore
  }
  return `Request failed (${response.status})`
}

export async function fetchQuestions(query?: string): Promise<Question[]> {
  const url = query && query.trim()
    ? `/api/questions?q=${encodeURIComponent(query.trim())}`
    : '/api/questions'
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(await parseError(response))
  }
  return response.json()
}

export async function createQuestion(input: QuestionInput): Promise<Question> {
  const response = await fetch('/api/questions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new Error(await parseError(response))
  }
  return response.json()
}

export async function updateQuestion(id: number, input: QuestionInput): Promise<Question> {
  const response = await fetch(`/api/questions/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new Error(await parseError(response))
  }
  return response.json()
}

export async function deleteQuestion(id: number): Promise<void> {
  const response = await fetch(`/api/questions/${id}`, { method: 'DELETE' })
  if (!response.ok) {
    throw new Error(await parseError(response))
  }
}
