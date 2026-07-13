import type { ExamResult } from '../types'

function optionText(answer: ExamResult['answers'][number], option: string | null) {
  if (!option) return 'Unanswered'
  return `${option}: ${answer[`option_${option.toLowerCase()}` as 'option_a' | 'option_b' | 'option_c' | 'option_d']}`
}
export function ExamResultsPage({ quizName, result, onBack, onRetry }: { quizName: string; result: ExamResult; onBack: () => void; onRetry: () => void }) {
  const incorrect = result.total - result.score
  return <section className="results-view"><p className="muted">{quizName}</p><h2>Exam Complete!</h2><div className="score-card"><div className="score-dial">{result.percentage}%<small>{result.score} / {result.total}</small></div><div><strong className="correct-count">{result.score} correct</strong><strong className="incorrect-count">{incorrect} incorrect</strong></div></div><div className="panel"><h3>Answer Review</h3>{result.answers.map((answer) => <article className={`answer-review ${answer.is_correct ? 'correct' : 'incorrect'}`} key={answer.question_id}><strong>{answer.is_correct ? '✓' : '✗'} {answer.question_text}</strong><p>Your answer: {optionText(answer, answer.selected_option)}</p>{!answer.is_correct && <p>Correct: {optionText(answer, answer.correct_option)}</p>}</article>)}</div><div className="page-actions"><button className="btn btn-secondary" onClick={onBack}>Back to Exams</button><button className="btn btn-primary" onClick={onRetry}>Retry Quiz</button></div></section>
}
