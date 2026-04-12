<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useTutorialStore } from '@/stores/tutorial'
import { useUserStore } from '@/stores/user'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG, getAvatarBg } from '@/utils'

const route = useRoute()
const router = useRouter()
const tutorialStore = useTutorialStore()
const userStore = useUserStore()

const tutorialId = computed(() => Number(route.params.id))
const tutorial = computed(() => tutorialStore.currentTutorial)
const loading = computed(() => tutorialStore.loading)
const completedCount = computed(
  () => tutorial.value?.chapters.filter((chapter) => chapter.isCompleted).length || 0
)

async function loadTutorial() {
  if (tutorialId.value) {
    await tutorialStore.fetchTutorialDetail(tutorialId.value)
  }
}

function startLearning() {
  if (!tutorial.value) return
  const targetChapter =
    tutorial.value.chapters.find((chapter) => !chapter.isCompleted) || tutorial.value.chapters[0]
  if (!targetChapter) return
  router.push(`/tutorials/${tutorialId.value}/learn/${targetChapter.id}`)
}

async function toggleCollect() {
  if (!tutorial.value) return
  if (!userStore.isLoggedIn) {
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }

  if (tutorial.value.isCollected) {
    await tutorialStore.uncollectTutorial(tutorial.value.id)
    ElMessage.success('已取消收藏')
  } else {
    await tutorialStore.collectTutorial(tutorial.value.id)
    ElMessage.success('收藏成功')
  }
}

onMounted(loadTutorial)
</script>

<template>
  <div class="page-shell">
    <div class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/tutorials">技能教程</RouterLink>
      <span>/</span>
      <span>{{ tutorial?.title || '教程详情' }}</span>
    </div>

    <div v-if="loading" class="state-card">正在加载教程详情...</div>

    <div v-else-if="tutorial" class="detail-grid">
      <section class="main-panel">
        <img :src="tutorial.coverImage" :alt="tutorial.title" class="hero-cover" />

        <div class="headline-card">
          <div class="tag-row">
            <span
              class="pill"
              :style="{ background: CATEGORY_CONFIG[tutorial.category]?.color || '#64748b' }"
            >
              {{ CATEGORY_CONFIG[tutorial.category]?.label || tutorial.category }}
            </span>
            <span
              class="pill pill-light"
              :style="{
                color: DIFFICULTY_CONFIG[tutorial.difficulty]?.color,
                background: DIFFICULTY_CONFIG[tutorial.difficulty]?.bgColor,
              }"
            >
              {{ DIFFICULTY_CONFIG[tutorial.difficulty]?.label }}
            </span>
          </div>

          <h1 class="page-title">{{ tutorial.title }}</h1>
          <p class="desc">{{ tutorial.description }}</p>

          <div class="stats-row">
            <span>作者：{{ tutorial.author }}</span>
            <span>浏览：{{ tutorial.viewCount }}</span>
            <span>收藏：{{ tutorial.collectCount }}</span>
            <span>评分：{{ tutorial.rating }}</span>
          </div>

          <div class="action-row">
            <button class="btn btn-primary" @click="startLearning">开始学习</button>
            <button class="btn btn-outline" @click="toggleCollect">
              {{ tutorial.isCollected ? '取消收藏' : '收藏教程' }}
            </button>
          </div>
        </div>

        <div class="section-card">
          <div class="section-head">
            <h2>章节列表</h2>
            <span>{{ completedCount }}/{{ tutorial.chapters.length }} 已完成</span>
          </div>

          <div class="chapter-list">
            <button
              v-for="(chapter, index) in tutorial.chapters"
              :key="chapter.id"
              class="chapter-item"
              @click="router.push(`/tutorials/${tutorial.id}/learn/${chapter.id}`)"
            >
              <div class="chapter-index">{{ index + 1 }}</div>
              <div class="chapter-main">
                <div class="chapter-title">{{ chapter.title }}</div>
                <div class="chapter-meta">
                  <span>{{ chapter.duration }}</span>
                  <span>{{ chapter.isFree ? '免费试看' : '正式章节' }}</span>
                  <span v-if="chapter.isCompleted" class="done">已完成</span>
                </div>
              </div>
            </button>
          </div>
        </div>
      </section>

      <aside class="side-panel">
        <div class="sidebar-card teacher-card">
          <div class="avatar" :style="{ background: getAvatarBg(tutorial.author) }">
            {{ tutorial.author?.[0] || 'A' }}
          </div>
          <div>
            <div class="teacher-name">{{ tutorial.author }}</div>
            <div class="teacher-desc">当前由 FastAPI 返回的讲师信息</div>
          </div>
        </div>

        <div class="sidebar-card">
          <h3>教程信息</h3>
          <div class="info-list">
            <div class="info-item">
              <span>学习时长</span>
              <strong>{{ tutorial.duration }}</strong>
            </div>
            <div class="info-item">
              <span>章节数量</span>
              <strong>{{ tutorial.chapters.length }}</strong>
            </div>
            <div class="info-item">
              <span>更新时间</span>
              <strong>{{ tutorial.updatedAt.slice(0, 10) }}</strong>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <div v-else class="state-card">没有找到对应教程。</div>
  </div>
</template>

<style scoped>
.page-shell {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.breadcrumb {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  color: var(--text-muted);
  font-size: 14px;
}

.breadcrumb a {
  color: var(--primary-color);
  text-decoration: none;
}

.detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: 24px;
  align-items: start;
}

.main-panel,
.side-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hero-cover {
  width: 100%;
  height: 320px;
  object-fit: cover;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.headline-card,
.section-card,
.sidebar-card,
.state-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.headline-card,
.section-card,
.sidebar-card {
  padding: 20px;
}

.tag-row,
.stats-row,
.action-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.tag-row {
  margin-bottom: 14px;
}

.page-title {
  margin: 0 0 12px;
  font-size: 30px;
  color: var(--text-primary);
}

.desc {
  margin: 0 0 16px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.stats-row {
  color: var(--text-muted);
  margin-bottom: 18px;
}

.pill {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}

.pill-light {
  color: var(--text-primary);
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-head h2 {
  margin: 0;
  font-size: 20px;
  color: var(--text-primary);
}

.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chapter-item {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  padding: 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-base);
  cursor: pointer;
  text-align: left;
}

.chapter-item:hover {
  border-color: var(--primary-color);
}

.chapter-index {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.chapter-main {
  flex: 1;
}

.chapter-title {
  color: var(--text-primary);
  font-weight: 700;
  margin-bottom: 6px;
}

.chapter-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  color: var(--text-muted);
  font-size: 14px;
}

.done {
  color: var(--color-success);
}

.teacher-card {
  display: flex;
  align-items: center;
  gap: 14px;
}

.avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 18px;
}

.teacher-name {
  color: var(--text-primary);
  font-weight: 700;
}

.teacher-desc {
  color: var(--text-muted);
  font-size: 14px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: var(--text-secondary);
}

.state-card {
  padding: 48px 20px;
  text-align: center;
  color: var(--text-muted);
}

@media (max-width: 960px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
