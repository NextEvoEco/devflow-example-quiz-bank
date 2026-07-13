export type Difficulty = 'Easy' | 'Medium' | 'Hard'
export type CorrectOption = 'A' | 'B' | 'C' | 'D'

export interface Question {
  id: number
  question: string
  option_a: string
  option_b: string
  option_c: string
  option_d: string
  correct: CorrectOption
  difficulty: Difficulty
  created_at?: string
  updated_at?: string
}

export type QuestionInput = Omit<Question, 'id' | 'created_at' | 'updated_at'> & {
  id?: number
  difficulty?: Difficulty | ''
}

export type PageId = 'questions' | 'quizList' | 'quizCreate' | 'examList' | 'examTaking' | 'examResults'

export interface QuizSummary {
  id: number
  name: string
  question_count: number
}

export interface Quiz extends QuizSummary {
  question_ids: number[]
  questions: Question[]
}

export interface ExamAnswer {
  question_id: number
  question_text: string
  selected_option: CorrectOption | null
  correct_option: CorrectOption
  is_correct: boolean
  option_a: string
  option_b: string
  option_c: string
  option_d: string
}

export interface ExamResult {
  score: number
  total: number
  percentage: number
  answers: ExamAnswer[]
}
