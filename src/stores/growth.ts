import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { PointRecord, Badge, GrowthData } from '@/types'
import api from '@/utils/request'

export const useGrowthStore = defineStore('growth', () => {
  const pointRecords = ref<PointRecord[]>([])
  const badges = ref<Badge[]>([])
  const growthData = ref<GrowthData[]>([])
  const loading = ref(false)

  const totalPoints = computed(() =>
    pointRecords.value.reduce((sum, r) => sum + r.points, 0)
  )

  const unlockedBadges = computed(() => badges.value.filter((b) => b.unlockedAt))
  const lockedBadges = computed(() => badges.value.filter((b) => !b.unlockedAt))

  async function fetchPointRecords() {
    loading.value = true
    try {
      const { data } = await api.get<PointRecord[]>('/points/records')
      pointRecords.value = data
    } finally {
      loading.value = false
    }
  }

  async function fetchBadges() {
    const { data } = await api.get<Badge[]>('/badges/my')
    badges.value = data
  }

  async function fetchGrowthData(days = 30) {
    const { data } = await api.get<GrowthData[]>(`/growth?days=${days}`)
    growthData.value = data
  }

  return {
    pointRecords,
    badges,
    growthData,
    loading,
    totalPoints,
    unlockedBadges,
    lockedBadges,
    fetchPointRecords,
    fetchBadges,
    fetchGrowthData,
  }
})
