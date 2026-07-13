<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { getQuiz, saveExamAnswer, startExamAttempt, submitExamAttempt } from '../api'
import type { ExamSubmitResult } from '../api'
import type { CorrectOption, Question } from '../types'

const props = defineProps<{
  quizId: number
}>()

const emit = defineEmits<{
  exit: []
  submitted: [result: ExamSubmitResult]
}>()

const attemptId = ref<number | null>(null)
const quizName = ref('')
const questions = ref<Question[]>([])
const index = ref(0)
const answers = ref<Record<number, CorrectOption>>({})
const error = ref('')
const busy = ref(false)

const current = computed(() => questions.value[index.value])
const progress = computed(() =>
  questions.value.length
    ? ((index.value + 1) / questions.value.length) * 100
    : 0,
)
const isLast = computed(() => index.value === questions.value.length - 1)

onMounted(async () => {
  try {
    const quiz = await getQuiz(props.quizId)
    quizName.value = quiz.name
    questions.value = quiz.questions
    const attempt = await startExamAttempt(props.quizId)
    attemptId.value = attempt.attempt_id
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to start exam'
  }
})

async function selectOption(option: CorrectOption) {
  if (!current.value || attemptId.value == null) return
  answers.value = { ...answers.value, [current.value.id]: option }
  try {
    await saveExamAnswer(attemptId.value, current.value.id, option)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to save answer'
  }
}

function previous() {
  if (index.value > 0) index.value -= 1
}

async function nextOrSubmit() {
  if (!isLast.value) {
    index.value += 1
    return
  }
  if (attemptId.value == null) return
  busy.value = true
  try {
    const result = await submitExamAttempt(attemptId.value)
    emit('submitted', result)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Submit failed'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <section class="page exam-taking-page">
    <div class="exam-header">
      <div>
        <p class="muted exam-label">{{ quizName }}</p>
        <p>Question {{ index + 1 }} of {{ questions.length || 0 }}</p>
      </div>
      <button type="button" class="btn btn-secondary" @click="emit('exit')">Exit</button>
    </div>
    <div class="progress-track">
      <div class="progress-fill" :style="{ width: `${progress}%` }" />
    </div>
    <p v-if="error" class="form-error">{{ error }}</p>

    <div v-if="current" class="exam-card">
      <h2>{{ current.question }}</h2>
      <button
        v-for="opt in (['A', 'B', 'C', 'D'] as CorrectOption[])"
        :key="opt"
        type="button"
        class="option-btn"
        :class="{ selected: answers[current.id] === opt }"
        @click="selectOption(opt)"
      >
        <span class="option-letter">{{ opt }}</span>
        <span>{{ current[opt.toLowerCase() as 'a' | 'b' | 'c' | 'd'] }}</span>
        <span v-if="answers[current.id] === opt" class="option-check">✓</span>
      </button>
    </div>

    <div class="exam-nav">
      <button
        type="button"
        class="btn btn-secondary"
        :style="{ opacity: index === 0 ? 0.3 : 1 }"
        @click="previous"
      >
        Previous
      </button>
      <button type="button" class="btn btn-primary" :disabled="busy" @click="nextOrSubmit">
        {{ isLast ? 'Submit' : 'Next' }}
      </button>
    </div>
  </section>
</template>
