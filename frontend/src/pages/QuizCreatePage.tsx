import { useEffect, useState } from 'react'
import { createQuiz, fetchQuiz, updateQuiz } from '../api/quizzes'
import { fetchQuestions } from '../api/questions'
import { DifficultyBadge } from '../components/DifficultyBadge'
import type { Question } from '../types'

export function QuizCreatePage({ quizId, onDone }: { quizId: number | null; onDone: () => void }) {
  const [name, setName] = useState('')
  const [questions, setQuestions] = useState<Question[]>([])
  const [selected, setSelected] = useState<Question[]>([])
  const [error, setError] = useState('')
  const [preview, setPreview] = useState(false)
  useEffect(() => {
    fetchQuestions().then(setQuestions).catch((e: Error) => setError(e.message))
    if (quizId) fetchQuiz(quizId).then((quiz) => { setName(quiz.name); setSelected(quiz.questions) }).catch((e: Error) => setError(e.message))
  }, [quizId])
  const move = (index: number, delta: number) => setSelected((items) => {
    const next = [...items]; const target = index + delta
    if (target >= 0 && target < next.length) [next[index], next[target]] = [next[target], next[index]]
    return next
  })
  async function save() {
    if (!name.trim()) return setError('Quiz name is required.')
    if (selected.length < 3) return setError('A quiz must include at least 3 questions.')
    try { quizId ? await updateQuiz(quizId, name, selected.map((q) => q.id)) : await createQuiz(name, selected.map((q) => q.id)); onDone() } catch (e) { setError((e as Error).message) }
  }
  const available = questions.filter((question) => !selected.some((item) => item.id === question.id))
  return <section className="builder">
    <button className="back-link" onClick={onDone}>← Back to Quizzes</button><h2>{quizId ? 'Edit Quiz' : 'New Quiz'}</h2>
    {error && <p className="error-banner">{error}</p>}
    <div className="panel form-field"><label>Quiz name<input value={name} onChange={(e) => setName(e.target.value)} /></label><label>Description<textarea rows={2} placeholder="Optional local-only description" /></label></div>
    <div className="panel"><h3>Selected Questions <span className="count-badge">{selected.length}</span></h3>
      {selected.length === 0 ? <p className="muted">No questions selected.</p> : selected.map((q, index) => <div className="question-row" key={q.id}><span>{index + 1}. {q.question}</span><DifficultyBadge difficulty={q.difficulty} /><button className="btn btn-secondary" disabled={index === 0} onClick={() => move(index, -1)}>↑</button><button className="btn btn-secondary" disabled={index === selected.length - 1} onClick={() => move(index, 1)}>↓</button><button className="icon-btn" onClick={() => setSelected(selected.filter((x) => x.id !== q.id))}>×</button></div>)}</div>
    <div className="panel"><h3>Add Questions</h3>{available.map((q) => <div className="question-row" key={q.id}><span>{q.question}</span><DifficultyBadge difficulty={q.difficulty} /><button className="btn btn-secondary" onClick={() => setSelected([...selected, q])}>Add</button></div>) || <p className="muted">All questions added.</p>}</div>
    <div className="page-actions"><button className="btn btn-secondary" onClick={onDone}>Cancel</button><button className="btn btn-secondary" onClick={() => setPreview(true)}>Preview</button><button className="btn btn-primary" onClick={save}>Save Quiz</button></div>
    {preview && <div className="modal-backdrop" onClick={() => setPreview(false)}><section className="modal modal-md" onClick={(e) => e.stopPropagation()}><div className="modal-header"><h2>Quiz Preview</h2><button className="icon-btn" onClick={() => setPreview(false)}>×</button></div><div className="modal-body">{selected.map((q, i) => <article key={q.id}><strong>{i + 1}. {q.question}</strong><p>A. {q.option_a}<br />B. {q.option_b}<br />C. {q.option_c}<br />D. {q.option_d}</p><p><strong>Correct: {q.correct}</strong></p></article>)}</div></section></div>}
  </section>
}
