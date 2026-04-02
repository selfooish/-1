import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Quiz, Question, QuizRecord } from '@/types'
import api from '@/utils/request'

export const useQuizStore = defineStore('quiz', () => {
  const quizList = ref<Quiz[]>([])
  const currentQuiz = ref<Quiz | null>(null)
  const questions = ref<Question[]>([])
  const quizRecords = ref<QuizRecord[]>([])
  const loading = ref(false)

  async function fetchQuizList(params?: { category?: string; keyword?: string; page?: number }) {
    loading.value = true
    try {
      const { data } = await api.get<{ list: Quiz[]; total: number }>('/quizzes', { params })
      quizList.value = data.list
    } finally {
      loading.value = false
    }
  }

  async function fetchQuizDetail(id: number) {
    loading.value = true
    try {
      const [quizRes, questionsRes] = await Promise.all([
        api.get<Quiz>(`/quizzes/${id}`),
        api.get<Question[]>(`/quizzes/${id}/questions`),
      ])
      currentQuiz.value = quizRes.data
      questions.value = questionsRes.data
    } finally {
      loading.value = false
    }
  }

  async function submitQuiz(quizId: number, answers: Record<number, string | string[]>) {
    const { data } = await api.post<QuizRecord>(`/quizzes/${quizId}/submit`, { answers })
    return data
  }

  async function fetchQuizRecords() {
    const { data } = await api.get<QuizRecord[]>('/quiz-records/my')
    quizRecords.value = data
  }

  return {
    quizList,
    currentQuiz,
    questions,
    quizRecords,
    loading,
    fetchQuizList,
    fetchQuizDetail,
    submitQuiz,
    fetchQuizRecords,
  }
})
