import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginForm, RegisterForm } from '@/types'
import { getLevelFromPoints } from '@/utils'
import api from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<User | null>(null)

  const isLoggedIn = computed(() => !!token.value)
  const levelInfo = computed(() =>
    userInfo.value ? getLevelFromPoints(userInfo.value.points) : null
  )

  async function login(form: LoginForm) {
    const { data } = await api.post<any>('/auth/login', form)
    token.value = data.token
    localStorage.setItem('token', data.token)
    userInfo.value = data.user
    return data
  }

  async function register(form: RegisterForm) {
    const { data } = await api.post<any>('/auth/register', form)
    token.value = data.token
    localStorage.setItem('token', data.token)
    userInfo.value = data.user
    return data
  }

  async function fetchUserInfo() {
    try {
      const { data } = await api.get<User>('/user/profile')
      userInfo.value = data
    } catch {
      // ignore
    }
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return { token, userInfo, isLoggedIn, levelInfo, login, register, fetchUserInfo, logout }
})
