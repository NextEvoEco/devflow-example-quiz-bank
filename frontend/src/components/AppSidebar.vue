<script setup lang="ts">
import { useAppState } from '../composables/useAppState'
import type { PageId } from '../types'

const { currentPage, navigate } = useAppState()

function isActive(section: 'questions' | 'quiz' | 'exam'): boolean {
  if (section === 'questions') return currentPage.value === 'questions'
  if (section === 'quiz') {
    return currentPage.value === 'quizList' || currentPage.value === 'quizCreate'
  }
  return (
    currentPage.value === 'examList' ||
    currentPage.value === 'examTaking' ||
    currentPage.value === 'examResults'
  )
}

function go(page: PageId) {
  navigate(page)
}
</script>

<template>
  <aside class="sidebar">
    <div class="logo">Quiz Bank</div>
    <nav class="nav">
      <button
        type="button"
        class="nav-item"
        :class="{ active: isActive('questions') }"
        @click="go('questions')"
      >
        Question Bank
      </button>
      <button
        type="button"
        class="nav-item"
        :class="{ active: isActive('quiz') }"
        @click="go('quizList')"
      >
        Quiz Builder
      </button>
      <button
        type="button"
        class="nav-item"
        :class="{ active: isActive('exam') }"
        @click="go('examList')"
      >
        Online Exam
      </button>
    </nav>
  </aside>
</template>
