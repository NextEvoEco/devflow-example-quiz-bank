import { useEffect, useState } from 'react'
import { fetchQuizzes } from '../api/quizzes'
import { EmptyState } from '../components/EmptyState'
import type { QuizSummary } from '../types'

export function ExamListPage({ onStart }: { onStart: (id: number) => void }) {
  const [quizzes, setQuizzes] = useState<QuizSummary[]>([])
  const [error, setError] = useState('')
  useEffect(() => { fetchQuizzes().then(setQuizzes).catch((e: Error) => setError(e.message)) }, [])
  return <section><h2>Available Exams</h2>{error && <p className="error-banner">{error}</p>}
    {!error && quizzes.length === 0 ? <EmptyState heading="No exams available" helper="Create a quiz in Quiz Builder first." /> :
      <div className="card-grid">{quizzes.map((quiz) => <article className="quiz-card" key={quiz.id}><strong>{quiz.name}</strong><p className="muted">{quiz.question_count} questions</p><button className="btn btn-primary full-width" onClick={() => onStart(quiz.id)}>Start Exam</button></article>)}</div>}
  </section>
}
