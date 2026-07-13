import { useState } from 'react'
import './App.css'
import { createQuestion, deleteQuestion, updateQuestion } from './api/questions'
import { startAttempt } from './api/exams'
import { fetchQuiz } from './api/quizzes'
import { AppShell } from './components/AppShell'
import { ConfirmDeleteDialog } from './components/ConfirmDeleteDialog'
import { QuestionEditorModal } from './components/QuestionEditorModal'
import { QuestionsPage } from './pages/QuestionsPage'
import { QuizListPage } from './pages/QuizListPage'
import { QuizCreatePage } from './pages/QuizCreatePage'
import { ExamListPage } from './pages/ExamListPage'
import { ExamTakingPage } from './pages/ExamTakingPage'
import { ExamResultsPage } from './pages/ExamResultsPage'
import type { ExamResult, PageId, Question, QuestionInput, Quiz } from './types'

function App() {
  const [refreshKey, setRefreshKey] = useState(0)
  const [editorMode, setEditorMode] = useState<'add' | 'edit' | null>(null)
  const [editing, setEditing] = useState<Question | null>(null)
  const [deleting, setDeleting] = useState<Question | null>(null)
  const [currentPage, setCurrentPage] = useState<PageId>('questions')
  const [quizId, setQuizId] = useState<number | null>(null)
  const [examQuiz, setExamQuiz] = useState<Quiz | null>(null)
  const [attemptId, setAttemptId] = useState<number | null>(null)
  const [result, setResult] = useState<ExamResult | null>(null)
  const [appError, setAppError] = useState('')

  function refresh() {
    setRefreshKey((value) => value + 1)
  }

  async function handleSave(input: QuestionInput) {
    if (editorMode === 'edit' && editing) {
      await updateQuestion(editing.id, input)
    } else {
      await createQuestion(input)
    }
    refresh()
  }

  const titles: Record<PageId, string> = { questions: 'Question Bank', quizList: 'Quiz Builder', quizCreate: 'Quiz Builder', examList: 'Online Exam', examTaking: 'Online Exam', examResults: 'Online Exam' }
  function navigate(page: PageId) {
    setCurrentPage(page)
    if (page !== 'examTaking') setAttemptId(null)
  }
  async function startExam(id: number) {
    try {
      const [quiz, attempt] = await Promise.all([fetchQuiz(id), startAttempt(id)])
      setExamQuiz(quiz); setAttemptId(attempt); setCurrentPage('examTaking')
    } catch (e) { setAppError((e as Error).message) }
  }
  const questionPage = <QuestionsPage
        refreshKey={refreshKey}
        onAdd={() => {
          setEditing(null)
          setEditorMode('add')
        }}
        onEdit={(question) => {
          setEditing(question)
          setEditorMode('edit')
        }}
        onDelete={(question) => setDeleting(question)}
      />
  return (
    <AppShell title={titles[currentPage]} currentPage={currentPage} onNavigate={navigate}>
      {appError && <p className="error-banner">{appError}</p>}
      {currentPage === 'questions' ? questionPage : null}
      {currentPage === 'quizList' ? <QuizListPage refreshKey={refreshKey} onCreate={() => { setQuizId(null); setCurrentPage('quizCreate') }} onEdit={(id) => { setQuizId(id); setCurrentPage('quizCreate') }} /> : null}
      {currentPage === 'quizCreate' ? <QuizCreatePage quizId={quizId} onDone={() => { refresh(); setCurrentPage('quizList') }} /> : null}
      {currentPage === 'examList' ? <ExamListPage onStart={startExam} /> : null}
      {currentPage === 'examTaking' && examQuiz && attemptId ? <ExamTakingPage quiz={examQuiz} attemptId={attemptId} onExit={() => navigate('examList')} onResult={(value) => { setResult(value); setCurrentPage('examResults') }} /> : null}
      {currentPage === 'examResults' && examQuiz && result ? <ExamResultsPage quizName={examQuiz.name} result={result} onBack={() => navigate('examList')} onRetry={() => startExam(examQuiz.id)} /> : null}

      {currentPage === 'questions' && editorMode ? (
        <QuestionEditorModal
          mode={editorMode}
          initial={editing}
          onClose={() => {
            setEditorMode(null)
            setEditing(null)
          }}
          onSave={handleSave}
        />
      ) : null}

      {currentPage === 'questions' && deleting ? (
        <ConfirmDeleteDialog
          title="Delete Question"
          message="Delete this question? It will also be removed from any quizzes that include it."
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            await deleteQuestion(deleting.id)
            refresh()
          }}
        />
      ) : null}
    </AppShell>
  )
}

export default App
