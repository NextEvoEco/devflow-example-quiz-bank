export type Difficulty = 'Easy' | 'Medium' | 'Hard'
export type CorrectOption = 'A' | 'B' | 'C' | 'D'

export interface Question {
  id: number
  question: string
  a: string
  b: string
  c: string
  d: string
  correct: CorrectOption
  difficulty: Difficulty
}

export interface QuizSummary {
  id: number
  name: string
  created_at?: string
  question_count: number
}

export interface QuizDetail extends QuizSummary {
  question_ids: number[]
  questions: Question[]
}

export type PageId =
  | 'questions'
  | 'quizList'
  | 'quizCreate'
  | 'examList'
  | 'examTaking'
  | 'examResults'

export interface QuestionInput {
  question: string
  a: string
  b: string
  c: string
  d: string
  correct: CorrectOption
  difficulty?: Difficulty
}

export interface QuizInput {
  name: string
  question_ids: number[]
}
