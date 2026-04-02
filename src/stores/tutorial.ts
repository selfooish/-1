import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Tutorial, TutorialListItem, TutorialCategory } from '@/types'
import api from '@/utils/request'

export const useTutorialStore = defineStore('tutorial', () => {
  const tutorials = ref<TutorialListItem[]>([])
  const currentTutorial = ref<Tutorial | null>(null)
  const loading = ref(false)
  const total = ref(0)

  async function fetchTutorials(params?: {
    category?: TutorialCategory | ''
    difficulty?: string
    keyword?: string
    page?: number
    pageSize?: number
  }) {
    loading.value = true
    try {
      const { data } = await api.get<{ list: TutorialListItem[]; total: number }>(
        '/tutorials',
        { params }
      )
      tutorials.value = data.list
      total.value = data.total
    } finally {
      loading.value = false
    }
  }

  async function fetchTutorialDetail(id: number) {
    loading.value = true
    try {
      const { data } = await api.get<Tutorial>(`/tutorials/${id}`)
      currentTutorial.value = data
    } finally {
      loading.value = false
    }
  }

  async function collectTutorial(id: number) {
    await api.post(`/tutorials/${id}/collect`)
    const t = tutorials.value.find((t) => t.id === id)
    if (t) t.collectCount++
    if (currentTutorial.value?.id === id) currentTutorial.value.isCollected = true
  }

  async function uncollectTutorial(id: number) {
    await api.delete(`/tutorials/${id}/collect`)
    const t = tutorials.value.find((t) => t.id === id)
    if (t) t.collectCount--
    if (currentTutorial.value?.id === id) currentTutorial.value.isCollected = false
  }

  async function completeChapter(tutorialId: number, chapterId: number) {
    await api.post(`/tutorials/${tutorialId}/chapters/${chapterId}/complete`)
    const t = currentTutorial.value
    if (t) {
      const ch = t.chapters.find((c) => c.id === chapterId)
      if (ch) ch.isCompleted = true
    }
  }

  return {
    tutorials,
    currentTutorial,
    loading,
    total,
    fetchTutorials,
    fetchTutorialDetail,
    collectTutorial,
    uncollectTutorial,
    completeChapter,
  }
})
