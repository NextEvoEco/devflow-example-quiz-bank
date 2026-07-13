<script setup lang="ts">
import { computed } from 'vue'
import type { ExamSubmitResult } from '../api'

const props = defineProps<{
  result: ExamSubmitResult
}>()

const emit = defineEmits<{
  back: []
  retry: []
}>()

const ringColor = computed(() => {
  if (props.result.percentage >= 70) return '#2b8a3e'
  if (props.result.percentage >= 50) return '#e67700'
  return '#c92a2a'
})

const incorrect = computed(() => props.result.total - props.result.score)
const circumference = 2 * Math.PI * 54
const dash = computed(
  () => `${(props.result.percentage / 100) * circumference} ${circumference}`,
)
</script>

<template>
  <section class="page exam-results-page">
    <p class="muted exam-label">{{ result.quiz_name }}</p>
    <h2>Exam Complete!</h2>

    <div class="score-summary">
      <div class="score-ring">
        <svg viewBox="0 0 120 120" aria-hidden="true">
          <circle cx="60" cy="60" r="54" class="ring-bg" />
          <circle
            cx="60"
            cy="60"
            r="54"
            class="ring-fg"
            :stroke="ringColor"
            :stroke-dasharray="dash"
          />
        </svg>
        <div class="score-center">
          <strong>{{ result.percentage }}%</strong>
          <span>{{ result.score }} / {{ result.total }}</span>
        </div>
      </div>
      <div class="score-counts">
        <div class="count-correct">{{ result.score }} Correct</div>
        <div class="count-incorrect">{{ incorrect }} Incorrect</div>
      </div>
    </div>

    <div class="panel">
      <h3>Answer Review</h3>
      <ul class="review-list">
        <li v-for="answer in result.answers" :key="answer.question_id">
          <span class="review-icon" :class="answer.is_correct ? 'ok' : 'bad'">
            {{ answer.is_correct ? '✓' : '✗' }}
          </span>
          <div class="review-body">
            <p class="review-question">{{ answer.question_text }}</p>
            <p class="muted">
              Your answer:
              {{
                answer.selected_option
                  ? `${answer.selected_option}: ${answer.selected_text}`
                  : 'No answer'
              }}
              <template v-if="!answer.is_correct">
                · Correct: {{ answer.correct_option }}: {{ answer.correct_text }}
              </template>
            </p>
          </div>
          <span class="badge" :class="answer.is_correct ? 'badge-easy' : 'badge-hard'">
            {{ answer.is_correct ? 'Correct' : 'Incorrect' }}
          </span>
        </li>
      </ul>
    </div>

    <div class="form-actions form-actions-center">
      <button type="button" class="btn btn-secondary" @click="emit('back')">Back to Exams</button>
      <button type="button" class="btn btn-primary" @click="emit('retry')">Retry Quiz</button>
    </div>
  </section>
</template>
