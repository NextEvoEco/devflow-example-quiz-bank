<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { createQuiz, getQuiz, listQuestions, updateQuiz } from '../api'
import type { Question } from '../types'
import DifficultyBadge from '../components/DifficultyBadge.vue'

const props = defineProps<{
  quizId: number | null
}>()

const emit = defineEmits<{
  cancel: []
  saved: []
}>()

const name = ref('')
const allQuestions = ref<Question[]>([])
const selected = ref<Question[]>([])
const search = ref('')
const error = ref('')
const previewOpen = ref(false)
const loading = ref(false)

const available = computed(() => {
  const selectedIds = new Set(selected.value.map((q) => q.id))
  const term = search.value.trim().toLowerCase()
  return allQuestions.value.filter((q) => {
    if (selectedIds.has(q.id)) return false
    if (!term) return true
    return q.question.toLowerCase().includes(term)
  })
})

async function loadBank() {
  allQuestions.value = await listQuestions()
}

async function loadQuiz() {
  if (props.quizId == null) {
    name.value = ''
    selected.value = []
    return
  }
  loading.value = true
  try {
    const quiz = await getQuiz(props.quizId)
    name.value = quiz.name
    selected.value = [...quiz.questions]
  } finally {
    loading.value = false
  }
}

function addQuestion(question: Question) {
  if (selected.value.some((q) => q.id === question.id)) return
  selected.value = [...selected.value, question]
}

function removeQuestion(questionId: number) {
  selected.value = selected.value.filter((q) => q.id !== questionId)
}

function move(index: number, delta: number) {
  const target = index + delta
  if (target < 0 || target >= selected.value.length) return
  const copy = [...selected.value]
  const [item] = copy.splice(index, 1)
  copy.splice(target, 0, item)
  selected.value = copy
}

async function save() {
  error.value = ''
  if (!name.value.trim()) {
    error.value = 'Quiz name is required'
    return
  }
  if (selected.value.length < 3) {
    error.value = 'A quiz requires at least 3 questions'
    return
  }
  const payload = {
    name: name.value.trim(),
    question_ids: selected.value.map((q) => q.id),
  }
  try {
    if (props.quizId == null) {
      await createQuiz(payload)
    } else {
      await updateQuiz(props.quizId, payload)
    }
    emit('saved')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Save failed'
  }
}

watch(
  () => props.quizId,
  () => {
    void loadQuiz()
  },
)

onMounted(async () => {
  await loadBank()
  await loadQuiz()
})
</script>

<template>
  <section class="page quiz-create-page">
    <button type="button" class="back-link" @click="emit('cancel')">← Back to Quizzes</button>
    <h2>{{ quizId == null ? 'New Quiz' : 'Edit Quiz' }}</h2>
    <p v-if="loading" class="muted">Loading…</p>
    <p v-if="error" class="form-error">{{ error }}</p>

    <div class="panel">
      <label class="field">
        <span>Quiz name</span>
        <input v-model="name" type="text" required />
      </label>
    </div>

    <div class="panel">
      <div class="panel-header">
        <h3>Selected Questions</h3>
        <span class="count-badge">{{ selected.length }}</span>
      </div>
      <p v-if="selected.length === 0" class="muted">No questions selected</p>
      <ul v-else class="question-picker-list">
        <li v-for="(q, index) in selected" :key="q.id">
          <div class="picker-main">
            <span>{{ q.question }}</span>
            <DifficultyBadge :difficulty="q.difficulty" />
          </div>
          <div class="picker-actions">
            <button type="button" class="btn btn-secondary btn-sm" @click="move(index, -1)">↑</button>
            <button type="button" class="btn btn-secondary btn-sm" @click="move(index, 1)">↓</button>
            <button type="button" class="btn btn-danger-ghost btn-sm" @click="removeQuestion(q.id)">
              ×
            </button>
          </div>
        </li>
      </ul>
    </div>

    <div class="panel">
      <div class="panel-header">
        <h3>Add Questions</h3>
      </div>
      <div class="search-box">
        <span class="search-icon" aria-hidden="true">⌕</span>
        <input v-model="search" type="search" placeholder="Search questions..." />
      </div>
      <p v-if="available.length === 0" class="muted">All questions added or no matches found</p>
      <ul v-else class="question-picker-list">
        <li v-for="q in available" :key="q.id">
          <div class="picker-main">
            <span>{{ q.question }}</span>
            <DifficultyBadge :difficulty="q.difficulty" />
          </div>
          <button type="button" class="btn btn-secondary btn-sm" @click="addQuestion(q)">
            Add
          </button>
        </li>
      </ul>
    </div>

    <div class="form-actions">
      <button type="button" class="btn btn-secondary" @click="emit('cancel')">Cancel</button>
      <button type="button" class="btn btn-secondary" @click="previewOpen = true">Preview</button>
      <button type="button" class="btn btn-primary" @click="save">Save Quiz</button>
    </div>

    <div v-if="previewOpen" class="modal-backdrop" @click.self="previewOpen = false">
      <div class="modal modal-lg" role="dialog" aria-modal="true" aria-label="Quiz Preview">
        <header class="modal-header">
          <h2>Preview: {{ name || 'Untitled quiz' }}</h2>
          <button type="button" class="icon-btn" aria-label="Close" @click="previewOpen = false">
            ×
          </button>
        </header>
        <div class="modal-body">
          <p v-if="selected.length === 0" class="muted">No questions selected.</p>
          <article v-for="(q, index) in selected" :key="q.id" class="preview-question">
            <h3>{{ index + 1 }}. {{ q.question }}</h3>
            <ul>
              <li :class="{ correct: q.correct === 'A' }">A. {{ q.a }}</li>
              <li :class="{ correct: q.correct === 'B' }">B. {{ q.b }}</li>
              <li :class="{ correct: q.correct === 'C' }">C. {{ q.c }}</li>
              <li :class="{ correct: q.correct === 'D' }">D. {{ q.d }}</li>
            </ul>
            <p class="muted">Correct: {{ q.correct }}</p>
          </article>
        </div>
        <footer class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="previewOpen = false">
            Close
          </button>
        </footer>
      </div>
    </div>
  </section>
</template>
