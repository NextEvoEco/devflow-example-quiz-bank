<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { listQuestions } from '../api'
import type { Question } from '../types'
import DifficultyBadge from '../components/DifficultyBadge.vue'
import EmptyState from '../components/EmptyState.vue'

const emit = defineEmits<{
  add: []
  edit: [question: Question]
  delete: [question: Question]
}>()

const questions = ref<Question[]>([])
const search = ref('')
const loading = ref(false)
const error = ref('')

async function load() {
  loading.value = true
  error.value = ''
  try {
    questions.value = await listQuestions(search.value)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load questions'
  } finally {
    loading.value = false
  }
}

let debounceTimer: ReturnType<typeof setTimeout> | undefined
watch(search, () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    void load()
  }, 150)
})

onMounted(() => {
  void load()
})

defineExpose({ reload: load })
</script>

<template>
  <section class="page questions-page">
    <div class="page-header">
      <div class="page-header-left">
        <h2>Questions</h2>
        <span class="count-badge">{{ questions.length }}</span>
      </div>
      <button type="button" class="btn btn-primary" @click="emit('add')">Add Question</button>
    </div>

    <div class="search-box">
      <span class="search-icon" aria-hidden="true">⌕</span>
      <input
        v-model="search"
        type="search"
        placeholder="Search questions..."
        aria-label="Search questions"
      />
    </div>

    <p v-if="error" class="form-error">{{ error }}</p>
    <p v-else-if="loading" class="muted">Loading…</p>

    <EmptyState
      v-else-if="questions.length === 0"
      heading="No questions found"
      :message="
        search.trim()
          ? 'No questions match your search.'
          : 'Your question bank is empty. Add your first question to get started.'
      "
      action-label="Add Question"
      @action="emit('add')"
    />

    <table v-else class="question-table">
      <thead>
        <tr>
          <th>Question</th>
          <th>Difficulty</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="q in questions" :key="q.id">
          <td>{{ q.question }}</td>
          <td><DifficultyBadge :difficulty="q.difficulty" /></td>
          <td class="actions">
            <button type="button" class="btn btn-secondary btn-sm" @click="emit('edit', q)">
              Edit
            </button>
            <button type="button" class="btn btn-danger-ghost btn-sm" @click="emit('delete', q)">
              Del
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
