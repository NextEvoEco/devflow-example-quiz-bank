<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { listQuizzes } from '../api'
import type { QuizSummary } from '../types'
import EmptyState from '../components/EmptyState.vue'

const emit = defineEmits<{
  start: [quizId: number]
}>()

const quizzes = ref<QuizSummary[]>([])
const error = ref('')

onMounted(async () => {
  try {
    quizzes.value = await listQuizzes()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load exams'
  }
})
</script>

<template>
  <section class="page">
    <div class="page-header">
      <h2>Available Exams</h2>
    </div>
    <p v-if="error" class="form-error">{{ error }}</p>
    <EmptyState
      v-if="quizzes.length === 0"
      heading="No exams available"
      message="Create a quiz in Quiz Builder first, then return here to take it."
    />
    <div v-else class="card-grid">
      <article v-for="quiz in quizzes" :key="quiz.id" class="quiz-card">
        <div class="quiz-card-top">
          <h3>{{ quiz.name }}</h3>
          <span class="count-badge">{{ quiz.question_count }}</span>
        </div>
        <button type="button" class="btn btn-primary btn-block" @click="emit('start', quiz.id)">
          Start Exam
        </button>
      </article>
    </div>
  </section>
</template>
