import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Task, TaskSubmission } from '@/types'
import api from '@/utils/request'

export const useTaskStore = defineStore('task', () => {
  const taskList = ref<Task[]>([])
  const myTasks = ref<Task[]>([])
  const currentTask = ref<Task | null>(null)
  const loading = ref(false)

  async function fetchTaskList(params?: { category?: string; status?: string; page?: number }) {
    loading.value = true
    try {
      const { data } = await api.get<{ list: Task[]; total: number }>('/tasks', { params })
      taskList.value = data.list
    } finally {
      loading.value = false
    }
  }

  async function fetchMyTasks() {
    loading.value = true
    try {
      const { data } = await api.get<Task[]>('/tasks/my')
      myTasks.value = data
    } finally {
      loading.value = false
    }
  }

  async function fetchTaskDetail(id: number) {
    loading.value = true
    try {
      const { data } = await api.get<Task>(`/tasks/${id}`)
      currentTask.value = data
    } finally {
      loading.value = false
    }
  }

  async function submitTask(
    taskId: number,
    content: string,
    attachments: { name: string; url: string; type: string }[]
  ) {
    const { data } = await api.post<TaskSubmission>(`/tasks/${taskId}/submit`, {
      content,
      attachments,
    })
    const task = myTasks.value.find((t) => t.id === taskId)
    if (task) task.status = 'submitted'
    return data
  }

  return {
    taskList,
    myTasks,
    currentTask,
    loading,
    fetchTaskList,
    fetchMyTasks,
    fetchTaskDetail,
    submitTask,
  }
})
