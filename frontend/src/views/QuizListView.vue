<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { deleteQuiz, listQuizzes } from '../api'
import type { QuizSummary } from '../types'
import EmptyState from '../components/EmptyState.vue'

const emit = defineEmits<{
  create: []
  edit: [quizId: number]
}>()

const quizzes = ref<QuizSummary[]>([])
const error = ref('')
const deleteTarget = ref<QuizSummary | null>(null)

async function load() {
  error.value = ''
  try {
    quizzes.value = await listQuizzes()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load quizzes'
  }
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  try {
    await deleteQuiz(deleteTarget.value.id)
    deleteTarget.value = null
    await load()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Delete failed'
  }
}

onMounted(() => {
  void load()
})

defineExpose({ reload: load })
</script>

<template>
  <section class="page">
    <div class="page-header">
      <h2>Quizzes</h2>
      <button type="button" class="btn btn-primary" @click="emit('create')">New Quiz</button>
    </div>
    <p v-if="error" class="form-error">{{ error }}</p>

    <EmptyState
      v-if="quizzes.length === 0"
      heading="No quizzes yet"
      message="Create a quiz by selecting questions from the Question Bank."
      action-label="Create Quiz"
      @action="emit('create')"
    />

    <div v-else class="card-grid">
      <article v-for="quiz in quizzes" :key="quiz.id" class="quiz-card">
        <div class="quiz-card-top">
          <h3>{{ quiz.name }}</h3>
          <span class="count-badge">{{ quiz.question_count }}</span>
        </div>
        <div class="quiz-card-actions">
          <button type="button" class="btn btn-secondary" @click="emit('edit', quiz.id)">
            Edit
          </button>
          <button type="button" class="btn btn-danger-ghost" @click="deleteTarget = quiz">
            Delete
          </button>
        </div>
      </article>
    </div>

    <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null">
      <div class="modal modal-sm" role="dialog" aria-modal="true" aria-label="Delete Quiz">
        <div class="modal-body confirm-body">
          <div class="empty-icon" aria-hidden="true">!</div>
          <h2>Delete Quiz</h2>
          <p>Delete “{{ deleteTarget.name }}”? Questions in the bank are unaffected.</p>
        </div>
        <footer class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="deleteTarget = null">
            Cancel
          </button>
          <button type="button" class="btn btn-danger" @click="confirmDelete">Delete</button>
        </footer>
      </div>
    </div>
  </section>
</template>
