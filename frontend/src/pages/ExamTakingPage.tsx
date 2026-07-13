import { useState } from 'react'
import { saveAnswer, submitAttempt } from '../api/exams'
import type { CorrectOption, ExamResult, Quiz } from '../types'

const options: CorrectOption[] = ['A', 'B', 'C', 'D']
export function ExamTakingPage({ quiz, attemptId, onExit, onResult }: { quiz: Quiz; attemptId: number; onExit: () => void; onResult: (result: ExamResult) => void }) {
  const [index, setIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<number, CorrectOption>>({})
  const [error, setError] = useState('')
  const question = quiz.questions[index]
  async function answer(option: CorrectOption) {
    setAnswers({ ...answers, [question.id]: option })
    try { await saveAnswer(attemptId, question.id, option) } catch (e) { setError((e as Error).message) }
  }
  async function submit() { try { onResult(await submitAttempt(attemptId)) } catch (e) { setError((e as Error).message) } }
  return <section className="exam-view"><div className="exam-header"><span>{quiz.name} · Question {index + 1} of {quiz.questions.length}</span><button className="btn btn-secondary" onClick={onExit}>Exit</button></div><div className="progress"><span style={{ width: `${((index + 1) / quiz.questions.length) * 100}%` }} /></div>{error && <p className="error-banner">{error}</p>}<article className="panel"><h2>{question.question}</h2>{options.map((option) => <button className={`option-button ${answers[question.id] === option ? 'selected' : ''}`} key={option} onClick={() => answer(option)}><b>{option}</b>{question[`option_${option.toLowerCase()}` as 'option_a' | 'option_b' | 'option_c' | 'option_d']}</button>)}</article><div className="page-actions"><button className="btn btn-secondary" disabled={index === 0} onClick={() => setIndex(index - 1)}>Previous</button>{index === quiz.questions.length - 1 ? <button className="btn btn-primary" onClick={submit}>Submit</button> : <button className="btn btn-primary" onClick={() => setIndex(index + 1)}>Next</button>}</div></section>
}
