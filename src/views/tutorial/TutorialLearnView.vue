<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const tutorialId = Number(route.params.id)
const chapterId = Number(route.params.chapterId)

const chapters = ref([
  { id: 1, title: '第一章：电饭煲的基本结构', duration: '15:00', isFree: true, isCompleted: true },
  { id: 2, title: '第二章：常见故障类型与原因', duration: '20:30', isFree: true, isCompleted: true },
  { id: 3, title: '第三章：不通电故障维修演示', duration: '25:00', isFree: false, isCompleted: false },
  { id: 4, title: '第四章：加热异常问题排查', duration: '22:00', isFree: false, isCompleted: false },
  { id: 5, title: '第五章：安全注意事项与总结', duration: '18:00', isFree: false, isCompleted: false },
])

const currentChapter = ref(chapters.value.find(c => c.id === chapterId) || chapters.value[2])
const currentChapterIdx = ref(chapters.value.findIndex(c => c.id === chapterId) || 0)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(900) // 15 * 60
let timer: ReturnType<typeof setInterval> | null = null

function playVideo() {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    timer = setInterval(() => {
      currentTime.value++
      if (currentTime.value >= duration.value) {
        isPlaying.value = false
        markComplete()
      }
    }, 1000)
  } else {
    if (timer) clearInterval(timer)
  }
}

function markComplete() {
  currentChapter.value.isCompleted = true
  ElMessage.success('✅ 章节完成！继续下一章吧')
}

function prevChapter() {
  if (currentChapterIdx.value > 0) {
    currentChapterIdx.value--
    currentChapter.value = chapters.value[currentChapterIdx.value]
    currentTime.value = 0
    isPlaying.value = false
    router.replace(`/tutorials/${tutorialId}/learn/${currentChapter.value.id}`)
  }
}

function nextChapter() {
  if (currentChapterIdx.value < chapters.value.length - 1) {
    currentChapterIdx.value++
    currentChapter.value = chapters.value[currentChapterIdx.value]
    currentTime.value = 0
    isPlaying.value = false
    router.replace(`/tutorials/${tutorialId}/learn/${currentChapter.value.id}`)
  }
}

function formatTime(s: number) {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`
}

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="learn-view">
    <!-- 返回 -->
    <button class="back-btn" @click="router.push(`/tutorials/${tutorialId}`)">
      ← 返回教程详情
    </button>

    <div class="learn-grid">
      <!-- 主视频区 -->
      <div class="learn-main">
        <!-- 视频播放器 -->
        <div class="video-player">
          <div class="video-area">
            <div class="video-placeholder" @click="playVideo">
              <span v-if="!isPlaying" class="big-play-btn">▶</span>
              <div v-if="!isPlaying" class="video-cover-overlay" />
              <video
                v-if="false"
                :src="currentChapter.videoUrl"
                @click="playVideo"
              />
            </div>
            <!-- 进度条 -->
            <div class="video-controls">
              <button class="play-pause" @click="playVideo">
                {{ isPlaying ? '⏸' : '▶' }}
              </button>
              <span class="time-display">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
              <div class="progress-track">
                <div class="progress-played" :style="{ width: `${(currentTime / duration) * 100}%` }" />
              </div>
              <button class="btn btn-sm btn-primary" style="margin-left:12px" @click="markComplete">
                ✅ 标记完成
              </button>
            </div>
          </div>
        </div>

        <!-- 章节信息 -->
        <div class="chapter-info-section">
          <div class="chapter-header">
            <div>
              <div class="chapter-tag">第 {{ currentChapterIdx + 1 }} 章</div>
              <h1 class="chapter-title">{{ currentChapter.title }}</h1>
              <div class="chapter-meta">
                <span>⏱ {{ currentChapter.duration }}</span>
                <span v-if="currentChapter.isCompleted" class="done-tag">✅ 已完成</span>
              </div>
            </div>
            <div class="chapter-nav-btns">
              <button class="nav-btn" :disabled="currentChapterIdx === 0" @click="prevChapter">← 上一章</button>
              <button class="nav-btn" :disabled="currentChapterIdx === chapters.length - 1" @click="nextChapter">下一章 →</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 章节列表 -->
      <aside class="learn-sidebar">
        <div class="sidebar-header">
          <h3>📚 课程目录</h3>
          <span class="sidebar-progress">{{ chapters.filter(c => c.isCompleted).length }}/{{ chapters.length }}</span>
        </div>
        <div class="chapter-list">
          <button
            v-for="(ch, idx) in chapters"
            :key="ch.id"
            class="chapter-btn"
            :class="{ active: ch.id === currentChapter.id, completed: ch.isCompleted }"
            @click="router.push(`/tutorials/${tutorialId}/learn/${ch.id}`)"
          >
            <span class="ch-num">
              <span v-if="ch.isCompleted">✅</span>
              <span v-else>{{ idx + 1 }}</span>
            </span>
            <span class="ch-title">{{ ch.title }}</span>
            <span class="ch-duration">{{ ch.duration }}</span>
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.learn-view {
  max-width: 1400px;
  margin: 0 auto;
}

.back-btn {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 0.85rem;
  margin-bottom: 20px;
  transition: all 0.2s;
}

.back-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.learn-grid {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 24px;
  align-items: start;
}

/* Video Player */
.video-player {
  margin-bottom: 20px;
}

.video-area {
  background: #000;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.video-placeholder {
  aspect-ratio: 16/9;
  background: linear-gradient(135deg, #1a1a2e, #2d2d44);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  cursor: pointer;
}

.big-play-btn {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(66, 184, 131, 0.9);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  padding-left: 6px;
  box-shadow: 0 4px 20px rgba(66, 184, 131, 0.5);
  z-index: 2;
  transition: transform 0.2s;
}

.video-placeholder:hover .big-play-btn {
  transform: scale(1.1);
}

.video-cover-overlay {
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h60v60H0z' fill='rgba(255,255,255,0.03)'/%3E%3C/svg%3E");
}

.video-controls {
  background: #1a1a2e;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.play-pause {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  border: none;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  flex-shrink: 0;
}

.play-pause:hover {
  background: rgba(255,255,255,0.2);
}

.time-display {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: rgba(255,255,255,0.6);
  white-space: nowrap;
}

.progress-track {
  flex: 1;
  height: 4px;
  background: rgba(255,255,255,0.15);
  border-radius: 2px;
  overflow: hidden;
}

.progress-played {
  height: 100%;
  background: var(--primary-color);
  border-radius: 2px;
  transition: width 0.5s;
}

/* Chapter Info */
.chapter-info-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 20px;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.chapter-tag {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary-color);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 6px;
}

.chapter-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.chapter-meta {
  display: flex;
  gap: 12px;
  font-size: 0.82rem;
  color: var(--text-muted);
}

.done-tag {
  color: var(--color-success);
  font-weight: 600;
}

.chapter-nav-btns {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.nav-btn {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-btn:hover:not(:disabled) {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Sidebar */
.learn-sidebar {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  position: sticky;
  top: 80px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-header h3 {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-primary);
}

.sidebar-progress {
  font-size: 0.78rem;
  color: var(--primary-color);
  font-weight: 600;
}

.chapter-list {
  display: flex;
  flex-direction: column;
}

.chapter-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  border-bottom: 1px solid var(--border-color);
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.82rem;
}

.chapter-btn:last-child {
  border-bottom: none;
}

.chapter-btn:hover {
  background: var(--bg-soft);
}

.chapter-btn.active {
  background: rgba(66, 184, 131, 0.08);
  border-left: 3px solid var(--primary-color);
}

.chapter-btn.completed .ch-num {
  color: var(--color-success);
}

.ch-num {
  width: 24px;
  text-align: center;
  font-weight: 700;
  color: var(--text-muted);
  flex-shrink: 0;
}

.ch-title {
  flex: 1;
  color: var(--text-primary);
  line-height: 1.4;
}

.ch-duration {
  color: var(--text-muted);
  font-size: 0.72rem;
  flex-shrink: 0;
}

@media (max-width: 1024px) {
  .learn-grid {
    grid-template-columns: 1fr;
  }
  .learn-sidebar {
    position: static;
  }
}
</style>
