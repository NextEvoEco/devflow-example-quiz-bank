<script setup lang="ts">
import { ref } from 'vue'
import QuestionsView from './views/QuestionsView.vue'
import QuizListView from './views/QuizListView.vue'
import QuizCreateView from './views/QuizCreateView.vue'
import ExamListView from './views/ExamListView.vue'
import ExamTakingView from './views/ExamTakingView.vue'
import ExamResultsView from './views/ExamResultsView.vue'
import QuestionEditorModal from './components/QuestionEditorModal.vue'
import ConfirmDialog from './components/ConfirmDialog.vue'
import AppSidebar from './components/AppSidebar.vue'
import AppTopBar from './components/AppTopBar.vue'
import { createQuestion, deleteQuestion, updateQuestion } from './api'
import type { ExamSubmitResult } from './api'
import { useAppState } from './composables/useAppState'
import type { Question, QuestionInput } from './types'

const { currentPage, pageTitle, navigate } = useAppState()

const listRef = ref<InstanceType<typeof QuestionsView> | null>(null)
const editorOpen = ref(false)
const editorMode = ref<'add' | 'edit'>('add')
const editing = ref<Question | null>(null)
const editorRef = ref<InstanceType<typeof QuestionEditorModal> | null>(null)

const deleteOpen = ref(false)
const deleting = ref<Question | null>(null)

const editingQuizId = ref<number | null>(null)
const examQuizId = ref<number | null>(null)
const examResult = ref<ExamSubmitResult | null>(null)
const examSession = ref(0)

function openAdd() {
  editorMode.value = 'add'
  editing.value = null
  editorOpen.value = true
}

function openEdit(question: Question) {
  editorMode.value = 'edit'
  editing.value = question
  editorOpen.value = true
}

function openDelete(question: Question) {
  deleting.value = question
  deleteOpen.value = true
}

async function onSave(payload: QuestionInput) {
  try {
    if (editorMode.value === 'edit' && editing.value) {
      await updateQuestion(editing.value.id, payload)
    } else {
      await createQuestion(payload)
    }
    editorOpen.value = false
    await listRef.value?.reload()
  } catch (err) {
    editorRef.value?.setError(err instanceof Error ? err.message : 'Save failed')
  }
}

async function onConfirmDelete() {
  if (!deleting.value) return
  try {
    await deleteQuestion(deleting.value.id)
    deleteOpen.value = false
    deleting.value = null
    await listRef.value?.reload()
  } catch (err) {
    deleteOpen.value = false
    window.alert(err instanceof Error ? err.message : 'Delete failed')
  }
}

function openCreateQuiz() {
  editingQuizId.value = null
  navigate('quizCreate')
}

function openEditQuiz(quizId: number) {
  editingQuizId.value = quizId
  navigate('quizCreate')
}

function onQuizSaved() {
  editingQuizId.value = null
  navigate('quizList')
}

function onQuizCancel() {
  editingQuizId.value = null
  navigate('quizList')
}

function startExam(quizId: number) {
  examQuizId.value = quizId
  examResult.value = null
  examSession.value += 1
  navigate('examTaking')
}

function onExamSubmitted(result: ExamSubmitResult) {
  examResult.value = result
  navigate('examResults')
}

function exitExam() {
  examQuizId.value = null
  navigate('examList')
}

function retryExam() {
  if (examQuizId.value == null && examResult.value) {
    examQuizId.value = examResult.value.quiz_id
  }
  examResult.value = null
  examSession.value += 1
  navigate('examTaking')
}
</script>

<template>
  <div class="shell">
    <AppSidebar />
    <div class="main">
      <AppTopBar :title="pageTitle" />
      <main class="content">
        <QuestionsView
          v-if="currentPage === 'questions'"
          ref="listRef"
          @add="openAdd"
          @edit="openEdit"
          @delete="openDelete"
        />
        <QuizListView
          v-else-if="currentPage === 'quizList'"
          @create="openCreateQuiz"
          @edit="openEditQuiz"
        />
        <QuizCreateView
          v-else-if="currentPage === 'quizCreate'"
          :quiz-id="editingQuizId"
          @cancel="onQuizCancel"
          @saved="onQuizSaved"
        />
        <ExamListView v-else-if="currentPage === 'examList'" @start="startExam" />
        <ExamTakingView
          v-else-if="currentPage === 'examTaking' && examQuizId != null"
          :key="examSession"
          :quiz-id="examQuizId"
          @exit="exitExam"
          @submitted="onExamSubmitted"
        />
        <ExamResultsView
          v-else-if="currentPage === 'examResults' && examResult"
          :result="examResult"
          @back="exitExam"
          @retry="retryExam"
        />
      </main>
    </div>

    <QuestionEditorModal
      ref="editorRef"
      :open="editorOpen"
      :mode="editorMode"
      :initial="editing"
      @close="editorOpen = false"
      @save="onSave"
    />

    <ConfirmDialog
      :open="deleteOpen"
      title="Delete Question"
      message="Delete this question? It will also be removed from any quizzes that reference it."
      @cancel="deleteOpen = false"
      @confirm="onConfirmDelete"
    />
  </div>
</template>
