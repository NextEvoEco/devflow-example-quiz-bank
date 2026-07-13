import { describe, expect, it } from 'vitest'
import type { Question } from './types'

function filterQuestions(questions: Question[], query: string): Question[] {
  const needle = query.trim().toLowerCase()
  if (!needle) {
    return questions
  }
  return questions.filter((item) => item.question.toLowerCase().includes(needle))
}

describe('question list filtering helper', () => {
  const sample: Question[] = [
    {
      id: 1,
      question: 'Largest continent?',
      option_a: 'Asia',
      option_b: 'Africa',
      option_c: 'Europe',
      option_d: 'Oceania',
      correct: 'A',
      difficulty: 'Easy',
    },
    {
      id: 2,
      question: 'Longest river?',
      option_a: 'Nile',
      option_b: 'Amazon',
      option_c: 'Yangtze',
      option_d: 'Mississippi',
      correct: 'A',
      difficulty: 'Medium',
    },
  ]

  it('returns all when query is empty', () => {
    expect(filterQuestions(sample, '')).toHaveLength(2)
  })

  it('filters case-insensitively by question text', () => {
    expect(filterQuestions(sample, 'CONTINENT')).toEqual([sample[0]])
  })
})
