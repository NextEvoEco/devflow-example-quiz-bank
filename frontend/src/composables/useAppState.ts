import { computed, ref } from 'vue'
import type { PageId } from '../types'

const currentPage = ref<PageId>('questions')

const pageTitle = computed(() => {
  switch (currentPage.value) {
    case 'questions':
      return 'Questions'
    case 'quizList':
      return 'Quizzes'
    case 'quizCreate':
      return 'Quiz Builder'
    case 'examList':
      return 'Available Exams'
    case 'examTaking':
      return 'Exam'
    case 'examResults':
      return 'Exam Results'
    default:
      return 'Quiz Bank'
  }
})

export function useAppState() {
  function navigate(page: PageId) {
    currentPage.value = page
  }

  return {
    currentPage,
    pageTitle,
    navigate,
  }
}
