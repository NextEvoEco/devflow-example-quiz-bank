import type { Difficulty } from '../types'

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  const tone =
    difficulty === 'Easy' ? 'easy' : difficulty === 'Hard' ? 'hard' : 'medium'
  return <span className={`difficulty-badge ${tone}`}>{difficulty}</span>
}
