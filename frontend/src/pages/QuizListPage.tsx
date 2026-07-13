import { useEffect, useState } from 'react'
import { deleteQuiz, fetchQuizzes } from '../api/quizzes'
import { EmptyState } from '../components/EmptyState'
import type { QuizSummary } from '../types'

export function QuizListPage({ refreshKey, onCreate, onEdit }: { refreshKey: number; onCreate: () => void; onEdit: (id: number) => void }) {
  const [quizzes, setQuizzes] = useState<QuizSummary[]>([])
  const [error, setError] = useState('')
  const load = () => fetchQuizzes().then(setQuizzes).catch((e: Error) => setError(e.message))
  useEffect(() => { void load() }, [refreshKey])
  return <section>
    <div className="page-header"><h2>Quizzes</h2><button className="btn btn-primary" onClick={onCreate}>New Quiz</button></div>
    {error && <p className="error-banner">{error}</p>}
    {!error && quizzes.length === 0 ? <EmptyState heading="No quizzes yet" helper="Create a quiz from questions in your bank." actionLabel="Create Quiz" onAction={onCreate} /> :
      <div className="card-grid">{quizzes.map((quiz) => <article className="quiz-card" key={quiz.id}>
        <div><strong>{quiz.name}</strong><span className="count-badge">{quiz.question_count}</span></div>
        <p className="muted">Question count: {quiz.question_count}</p>
        <div className="card-actions"><button className="btn btn-secondary" onClick={() => onEdit(quiz.id)}>Edit</button>
          <button className="btn btn-danger" onClick={async () => { if (window.confirm(`Delete "${quiz.name}"?`)) { await deleteQuiz(quiz.id); load() } }}>Delete</button></div>
      </article>)}</div>}
  </section>
}
