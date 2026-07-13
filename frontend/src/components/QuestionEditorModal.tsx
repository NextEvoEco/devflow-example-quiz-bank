import { useState, type FormEvent } from 'react'
import type { CorrectOption, Difficulty, Question, QuestionInput } from '../types'

interface QuestionEditorModalProps {
  mode: 'add' | 'edit'
  initial?: Question | null
  onClose: () => void
  onSave: (input: QuestionInput) => Promise<void>
}

const EMPTY: QuestionInput = {
  question: '',
  option_a: '',
  option_b: '',
  option_c: '',
  option_d: '',
  correct: 'A',
  difficulty: 'Medium',
}

export function QuestionEditorModal({ mode, initial, onClose, onSave }: QuestionEditorModalProps) {
  const [form, setForm] = useState<QuestionInput>(
    initial
      ? {
          question: initial.question,
          option_a: initial.option_a,
          option_b: initial.option_b,
          option_c: initial.option_c,
          option_d: initial.option_d,
          correct: initial.correct,
          difficulty: initial.difficulty,
        }
      : EMPTY,
  )
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!form.question.trim()) {
      setError('Question text is required')
      return
    }
    setSaving(true)
    setError(null)
    try {
      await onSave(form)
      onClose()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Save failed')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose} role="presentation">
      <div
        className="modal modal-md"
        role="dialog"
        aria-modal="true"
        aria-labelledby="question-editor-title"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-header">
          <h2 id="question-editor-title">{mode === 'add' ? 'Add Question' : 'Edit Question'}</h2>
          <button type="button" className="icon-btn" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error ? <p className="error-banner">{error}</p> : null}
            <div className="form-field">
              <label htmlFor="question-text">Question text</label>
              <textarea
                id="question-text"
                rows={3}
                required
                value={form.question}
                onChange={(event) => setForm({ ...form, question: event.target.value })}
              />
            </div>
            {(['a', 'b', 'c', 'd'] as const).map((letter) => {
              const key = `option_${letter}` as const
              return (
                <div className="form-field" key={key}>
                  <label htmlFor={key}>Option {letter.toUpperCase()}</label>
                  <input
                    id={key}
                    required
                    value={form[key]}
                    onChange={(event) => setForm({ ...form, [key]: event.target.value })}
                  />
                </div>
              )
            })}
            <div className="form-field">
              <label htmlFor="correct">Correct Answer</label>
              <select
                id="correct"
                value={form.correct}
                onChange={(event) =>
                  setForm({ ...form, correct: event.target.value as CorrectOption })
                }
              >
                <option value="A">A</option>
                <option value="B">B</option>
                <option value="C">C</option>
                <option value="D">D</option>
              </select>
            </div>
            <div className="form-field">
              <label htmlFor="difficulty">Difficulty</label>
              <select
                id="difficulty"
                value={form.difficulty || 'Medium'}
                onChange={(event) =>
                  setForm({ ...form, difficulty: event.target.value as Difficulty })
                }
              >
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              Save Question
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
