<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useTutorialStore } from '@/stores/tutorial'

const route = useRoute()
const router = useRouter()
const tutorialStore = useTutorialStore()

const tutorialId = computed(() => Number(route.params.id))
const chapterId = computed(() => Number(route.params.chapterId))

const tutorial = computed(() => tutorialStore.currentTutorial)
const chapters = computed(() => tutorial.value?.chapters || [])
const loading = computed(() => tutorialStore.loading)

const currentIndex = ref(0)
const currentTime = ref(0)
const duration = ref(15 * 60)
const playing = ref(false)

let timer: ReturnType<typeof setInterval> | null = null

const currentChapter = computed(() => chapters.value[currentIndex.value])

function syncCurrentChapter() {
  const index = chapters.value.findIndex((chapter) => chapter.id === chapterId.value)
  currentIndex.value = index >= 0 ? index : 0
  currentTime.value = 0
  playing.value = false
}

async function loadTutorial() {
  if (!tutorialId.value) return
  await tutorialStore.fetchTutorialDetail(tutorialId.value)
  syncCurrentChapter()
}

function formatTime(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

function stopTimer() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

function togglePlay() {
  if (!currentChapter.value) return

  if (playing.value) {
    playing.value = false
    stopTimer()
    return
  }

  playing.value = true
  timer = setInterval(() => {
    currentTime.value += 1
    if (currentTime.value >= duration.value) {
      playing.value = false
      stopTimer()
      markComplete()
    }
  }, 1000)
}

async function markComplete() {
  if (!currentChapter.value || !tutorial.value) return
  await tutorialStore.completeChapter(tutorial.value.id, currentChapter.value.id)
  ElMessage.success('章节进度已同步')
}

function jumpToChapter(index: number) {
  const chapter = chapters.value[index]
  if (!chapter) return
  router.replace(`/tutorials/${tutorialId.value}/learn/${chapter.id}`)
}

watch([tutorialId, chapterId], loadTutorial)

onMounted(loadTutorial)

onBeforeUnmount(() => {
  stopTimer()
})
</script>

<template>
  <div class="learn-shell">
    <button class="back-btn" @click="router.push(`/tutorials/${tutorialId}`)">返回教程详情</button>

    <div v-if="loading" class="state-card">正在加载学习内容...</div>

    <div v-else-if="tutorial && currentChapter" class="learn-grid">
      <section class="main-panel">
        <div class="video-card">
          <div class="video-stage" @click="togglePlay">
            <div class="play-icon">{{ playing ? '暂停' : '播放' }}</div>
          </div>

          <div class="video-controls">
            <button class="btn btn-outline btn-sm" @click="togglePlay">
              {{ playing ? '暂停' : '播放' }}
            </button>
            <span>{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: `${(currentTime / duration) * 100}%` }" />
            </div>
            <button class="btn btn-primary btn-sm" @click="markComplete">标记完成</button>
          </div>
        </div>

        <div class="info-card">
          <div class="chapter-tag">第 {{ currentIndex + 1 }} 章</div>
          <h1>{{ currentChapter.title }}</h1>
          <div class="meta-row">
            <span>时长 {{ currentChapter.duration }}</span>
            <span>{{ currentChapter.isFree ? '免费章节' : '正式章节' }}</span>
            <span v-if="currentChapter.isCompleted" class="done">已完成</span>
          </div>
        </div>
      </section>

      <aside class="side-panel">
        <div class="list-card">
          <div class="list-head">
            <h3>章节目录</h3>
            <span>{{ chapters.filter((item) => item.isCompleted).length }}/{{ chapters.length }}</span>
          </div>

          <div class="chapter-list">
            <button
              v-for="(chapter, index) in chapters"
              :key="chapter.id"
              class="chapter-item"
              :class="{ active: index === currentIndex, done: chapter.isCompleted }"
              @click="jumpToChapter(index)"
            >
              <span class="chapter-index">{{ index + 1 }}</span>
              <span class="chapter-name">{{ chapter.title }}</span>
            </button>
          </div>
        </div>
      </aside>
    </div>

    <div v-else class="state-card">没有找到当前章节。</div>
  </div>
</template>

<style scoped>
.learn-shell {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.back-btn {
  align-self: flex-start;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
}

.learn-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: 20px;
}

.main-panel,
.side-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.video-card,
.info-card,
.list-card,
.state-card {
  padding: 20px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.video-stage {
  height: 360px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, #0f172a, #1e293b);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.play-icon {
  padding: 14px 22px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-weight: 700;
}

.video-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.progress-track {
  flex: 1;
  height: 6px;
  border-radius: 999px;
  background: var(--bg-soft);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary-color);
}

.chapter-tag {
  margin-bottom: 10px;
  color: var(--primary-color);
  font-size: 13px;
  font-weight: 700;
}

.info-card h1 {
  margin: 0 0 12px;
  color: var(--text-primary);
  font-size: 28px;
}

.meta-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  color: var(--text-muted);
}

.done {
  color: var(--color-success);
}

.list-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.list-head h3 {
  margin: 0;
  color: var(--text-primary);
}

.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chapter-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-base);
  text-align: left;
  cursor: pointer;
}

.chapter-item.active {
  border-color: var(--primary-color);
  background: rgba(66, 184, 131, 0.08);
}

.chapter-item.done .chapter-name {
  color: var(--primary-color);
}

.chapter-index {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--bg-soft);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.chapter-name {
  color: var(--text-primary);
}

.state-card {
  text-align: center;
  color: var(--text-muted);
}

@media (max-width: 960px) {
  .learn-grid {
    grid-template-columns: 1fr;
  }
}
</style>
