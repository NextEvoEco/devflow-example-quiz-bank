import { useEffect, useState } from 'react'
import { fetchQuestions } from '../api/questions'
import type { Question } from '../types'
import { DifficultyBadge } from '../components/DifficultyBadge'
import { EmptyState } from '../components/EmptyState'

interface QuestionsPageProps {
  onAdd: () => void
  onEdit: (question: Question) => void
  onDelete: (question: Question) => void
  refreshKey: number
}

export function QuestionsPage({ onAdd, onEdit, onDelete, refreshKey }: QuestionsPageProps) {
  const [query, setQuery] = useState('')
  const [questions, setQuestions] = useState<Question[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    const handle = window.setTimeout(() => {
      fetchQuestions(query)
        .then((data) => {
          if (!cancelled) {
            setQuestions(data)
          }
        })
        .catch((err: Error) => {
          if (!cancelled) {
            setError(err.message)
          }
        })
        .finally(() => {
          if (!cancelled) {
            setLoading(false)
          }
        })
    }, 150)

    return () => {
      cancelled = true
      window.clearTimeout(handle)
    }
  }, [query, refreshKey])

  return (
    <section className="questions-page">
      <div className="page-header">
        <div className="page-header-left">
          <h2>Questions</h2>
          <span className="count-badge">{questions.length}</span>
        </div>
        <button type="button" className="btn btn-primary" onClick={onAdd}>
          Add Question
        </button>
      </div>

      <div className="search-row">
        <input
          className="search-input"
          type="search"
          placeholder="Search questions..."
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          aria-label="Search questions"
        />
      </div>

      {error ? <p className="error-banner">{error}</p> : null}
      {loading ? <p className="muted">Loading...</p> : null}

      {!loading && !error && questions.length === 0 ? (
        <EmptyState
          heading="No questions found"
          helper={
            query
              ? 'Try a different search term, or add a new question.'
              : 'Your question bank is empty. Add your first question to get started.'
          }
          actionLabel="Add Question"
          onAction={onAdd}
        />
      ) : null}

      {!loading && questions.length > 0 ? (
        <table className="questions-table">
          <thead>
            <tr>
              <th>Question</th>
              <th>Difficulty</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {questions.map((question) => (
              <tr key={question.id}>
                <td>{question.question}</td>
                <td>
                  <DifficultyBadge difficulty={question.difficulty} />
                </td>
                <td className="actions-cell">
                  <button type="button" className="btn btn-secondary" onClick={() => onEdit(question)}>
                    Edit
                  </button>
                  <button type="button" className="btn btn-danger" onClick={() => onDelete(question)}>
                    Del
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </section>
  )
}
