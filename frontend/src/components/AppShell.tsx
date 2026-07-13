import type { ReactNode } from 'react'
import type { PageId } from '../types'

interface AppShellProps {
  title: string
  children: ReactNode
  currentPage: PageId
  onNavigate: (page: PageId) => void
}

export function AppShell({ title, children, currentPage, onNavigate }: AppShellProps) {
  const quizActive = currentPage === 'quizList' || currentPage === 'quizCreate'
  const examActive = currentPage === 'examList' || currentPage === 'examTaking' || currentPage === 'examResults'
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="logo">Quiz Bank</div>
        <nav className="sidebar-nav">
          <button type="button" className={`nav-item ${currentPage === 'questions' ? 'active' : ''}`} onClick={() => onNavigate('questions')}>
            Question Bank
          </button>
          <button type="button" className={`nav-item ${quizActive ? 'active' : ''}`} onClick={() => onNavigate('quizList')}>
            Quiz Builder
          </button>
          <button type="button" className={`nav-item ${examActive ? 'active' : ''}`} onClick={() => onNavigate('examList')}>
            Online Exam
          </button>
        </nav>
      </aside>
      <div className="main">
        <header className="topbar">
          <h1>{title}</h1>
        </header>
        <main className="content">{children}</main>
      </div>
    </div>
  )
}
