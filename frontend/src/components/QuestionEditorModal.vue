<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import type { CorrectOption, Difficulty, Question, QuestionInput } from '../types'

const props = defineProps<{
  open: boolean
  mode: 'add' | 'edit'
  initial?: Question | null
}>()

const emit = defineEmits<{
  close: []
  save: [payload: QuestionInput]
}>()

const form = reactive<QuestionInput>({
  question: '',
  a: '',
  b: '',
  c: '',
  d: '',
  correct: 'A',
  difficulty: 'Medium',
})

const error = ref('')

const title = computed(() => (props.mode === 'add' ? 'Add Question' : 'Edit Question'))

function resetFromInitial() {
  error.value = ''
  if (props.mode === 'edit' && props.initial) {
    form.question = props.initial.question
    form.a = props.initial.a
    form.b = props.initial.b
    form.c = props.initial.c
    form.d = props.initial.d
    form.correct = props.initial.correct
    form.difficulty = props.initial.difficulty
  } else {
    form.question = ''
    form.a = ''
    form.b = ''
    form.c = ''
    form.d = ''
    form.correct = 'A'
    form.difficulty = 'Medium'
  }
}

watch(
  () => props.open,
  (open) => {
    if (open) resetFromInitial()
  },
)

function onBackdrop() {
  emit('close')
}

function onSave() {
  if (!form.question.trim()) {
    error.value = 'Question text is required'
    return
  }
  if (![form.a, form.b, form.c, form.d].every((v) => v.trim())) {
    error.value = 'Options A–D are required'
    return
  }
  emit('save', {
    question: form.question.trim(),
    a: form.a.trim(),
    b: form.b.trim(),
    c: form.c.trim(),
    d: form.d.trim(),
    correct: form.correct as CorrectOption,
    difficulty: form.difficulty as Difficulty,
  })
}

function setError(message: string) {
  error.value = message
}

defineExpose({ setError })
</script>

<template>
  <div v-if="open" class="modal-backdrop" @click.self="onBackdrop">
    <div class="modal" role="dialog" aria-modal="true" :aria-label="title">
      <header class="modal-header">
        <h2>{{ title }}</h2>
        <button type="button" class="icon-btn" aria-label="Close" @click="emit('close')">×</button>
      </header>
      <div class="modal-body">
        <p v-if="error" class="form-error">{{ error }}</p>
        <label class="field">
          <span>Question text</span>
          <textarea v-model="form.question" rows="3" required />
        </label>
        <label class="field">
          <span>Option A</span>
          <input v-model="form.a" type="text" required />
        </label>
        <label class="field">
          <span>Option B</span>
          <input v-model="form.b" type="text" required />
        </label>
        <label class="field">
          <span>Option C</span>
          <input v-model="form.c" type="text" required />
        </label>
        <label class="field">
          <span>Option D</span>
          <input v-model="form.d" type="text" required />
        </label>
        <label class="field">
          <span>Correct Answer</span>
          <select v-model="form.correct">
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
          </select>
        </label>
        <label class="field">
          <span>Difficulty</span>
          <select v-model="form.difficulty">
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </label>
      </div>
      <footer class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="emit('close')">Cancel</button>
        <button type="button" class="btn btn-primary" @click="onSave">Save Question</button>
      </footer>
    </div>
  </div>
</template>
