<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG, getAvatarBg } from '@/utils'
import { ElMessage } from 'element-plus'
import type { Tutorial } from '@/types'

const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)

const tutorial = ref<Tutorial>({
  id: 1,
  title: '电饭煲常见故障与维修',
  category: '家电维修',
  coverImage: 'https://picsum.photos/seed/elec/800/450',
  description: '本教程详细讲解电饭煲的常见故障与维修方法，包括不通电、加热异常、漏电等问题的诊断与修复。通过本教程，你将掌握电饭煲的基本结构、常见故障排查流程，以及安全维修注意事项。',
  duration: '2h30m',
  difficulty: 'medium',
  author: '王师傅',
  authorAvatar: '',
  viewCount: 2341,
  collectCount: 156,
  isCollected: false,
  isPurchased: true,
  tags: ['家电维修', '动手实践', '安全第一'],
  chapters: [
    { id: 1, title: '第一章：电饭煲的基本结构', duration: '15:00', isFree: true, isCompleted: true, videoUrl: '' },
    { id: 2, title: '第二章：常见故障类型与原因', duration: '20:30', isFree: true, isCompleted: true, videoUrl: '' },
    { id: 3, title: '第三章：不通电故障维修演示', duration: '25:00', isFree: false, isCompleted: false, videoUrl: '' },
    { id: 4, title: '第四章：加热异常问题排查', duration: '22:00', isFree: false, isCompleted: false, videoUrl: '' },
    { id: 5, title: '第五章：安全注意事项与总结', duration: '18:00', isFree: false, isCompleted: false, videoUrl: '' },
  ],
  rating: 4.8,
  reviewCount: 156,
  createdAt: '2024-09-01',
  updatedAt: '2024-12-01',
})

const isCollected = ref(false)

function startLearning() {
  const firstChapter = tutorial.value.chapters.find(c => c.isFree && !c.isCompleted) || tutorial.value.chapters[0]
  router.push(`/tutorials/${id}/learn/${firstChapter.id}`)
}

function toggleCollect() {
  isCollected.value = !isCollected.value
  ElMessage.success(isCollected.value ? '已收藏' : '已取消收藏')
}

const completedCount = ref(2)
</script>

<template>
  <div class="tutorial-detail-view">
    <!-- 面包屑 -->
    <div class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span> / </span>
      <RouterLink to="/tutorials">技能教程</RouterLink>
      <span> / </span>
      <span>{{ tutorial.category }}</span>
      <span> / </span>
      <span class="current">{{ tutorial.title }}</span>
    </div>

    <div class="detail-grid">
      <!-- 左：内容 -->
      <div class="detail-main">
        <!-- 封面图 -->
        <div class="cover-section">
          <img :src="tutorial.coverImage" :alt="tutorial.title" class="cover-img" />
          <div class="cover-overlay">
            <div class="cover-meta">
              <span class="badge" :style="{ background: DIFFICULTY_CONFIG[tutorial.difficulty]?.bgColor, color: DIFFICULTY_CONFIG[tutorial.difficulty]?.color }">
                {{ DIFFICULTY_CONFIG[tutorial.difficulty]?.label }}
              </span>
              <span class="cover-duration">⏱ {{ tutorial.duration }}</span>
              <span class="cover-views">👁 {{ tutorial.viewCount }}</span>
            </div>
            <button class="start-learn-btn" @click="startLearning">
              <span>▶</span> 开始学习
            </button>
          </div>
        </div>

        <!-- 标题与操作 -->
        <div class="tutorial-header">
          <div class="header-top">
            <span class="category-tag" :style="{ background: CATEGORY_CONFIG[tutorial.category]?.color }">
              {{ CATEGORY_CONFIG[tutorial.category]?.icon }} {{ tutorial.category }}
            </span>
            <div class="header-actions">
              <button class="action-btn" :class="{ collected: isCollected }" @click="toggleCollect">
                {{ isCollected ? '❤️' : '🤍' }} {{ isCollected ? '已收藏' : '收藏' }}
              </button>
              <button class="action-btn">📤 分享</button>
            </div>
          </div>
          <h1 class="tutorial-title">{{ tutorial.title }}</h1>
          <div class="tutorial-rating">
            <span class="stars">⭐⭐⭐⭐⭐</span>
            <span>{{ tutorial.rating }}</span>
            <span>({{ tutorial.reviewCount }} 条评价)</span>
          </div>
          <p class="tutorial-desc">{{ tutorial.description }}</p>
          <div class="tags">
            <span v-for="tag in tutorial.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>

        <!-- 章节列表 -->
        <div class="chapters-section">
          <h2 class="section-title">
            📚 课程章节
            <span class="chapter-progress">{{ completedCount }}/{{ tutorial.chapters.length }} 已完成</span>
          </h2>
          <div class="chapters-list">
            <div
              v-for="(chapter, idx) in tutorial.chapters"
              :key="chapter.id"
              class="chapter-item"
              :class="{ completed: chapter.isCompleted, locked: !chapter.isFree && !tutorial.isPurchased }"
              @click="chapter.isFree || tutorial.isPurchased ? router.push(`/tutorials/${id}/learn/${chapter.id}`) : null"
            >
              <div class="chapter-number">
                <span v-if="chapter.isCompleted" class="check-icon">✅</span>
                <span v-else-if="!chapter.isFree && !tutorial.isPurchased" class="lock-icon">🔒</span>
                <span v-else>{{ idx + 1 }}</span>
              </div>
              <div class="chapter-info">
                <div class="chapter-title">{{ chapter.title }}</div>
                <div class="chapter-meta">
                  <span>{{ chapter.duration }}</span>
                  <span v-if="chapter.isFree" class="free-tag">免费</span>
                  <span v-else-if="!tutorial.isPurchased" class="lock-tag">需购买</span>
                </div>
              </div>
              <button v-if="chapter.isFree || tutorial.isPurchased" class="chapter-play">
                {{ chapter.isCompleted ? '🔄 重新学习' : '▶ 开始' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 右：侧栏 -->
      <aside class="detail-sidebar">
        <div class="author-card">
          <div class="author-avatar" :style="{ background: getAvatarBg(tutorial.author) }">
            {{ tutorial.author[0] }}
          </div>
          <div class="author-info">
            <div class="author-name">{{ tutorial.author }}</div>
            <div class="author-title">资深维修技师</div>
          </div>
        </div>

        <div class="info-card">
          <h3>课程信息</h3>
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">难度</span>
              <span class="info-value" :style="{ color: DIFFICULTY_CONFIG[tutorial.difficulty]?.color }">
                {{ DIFFICULTY_CONFIG[tutorial.difficulty]?.label }}
              </span>
            </div>
            <div class="info-item">
              <span class="info-label">时长</span>
              <span class="info-value">{{ tutorial.duration }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">章节</span>
              <span class="info-value">{{ tutorial.chapters.length }} 节</span>
            </div>
            <div class="info-item">
              <span class="info-label">观看</span>
              <span class="info-value">{{ tutorial.viewCount }} 人</span>
            </div>
            <div class="info-item">
              <span class="info-label">收藏</span>
              <span class="info-value">{{ tutorial.collectCount }} 人</span>
            </div>
          </div>
        </div>

        <div class="progress-card">
          <h3>学习进度</h3>
          <div class="progress-bar-wrap">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${(completedCount / tutorial.chapters.length) * 100}%` }" />
            </div>
            <span class="progress-text">{{ Math.round((completedCount / tutorial.chapters.length) * 100) }}%</span>
          </div>
          <div class="progress-desc">{{ completedCount }}/{{ tutorial.chapters.length }} 章节已完成</div>
          <button class="btn btn-primary" style="width:100%;margin-top:12px" @click="startLearning">
            {{ completedCount > 0 ? '继续学习' : '开始学习' }}
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.tutorial-detail-view {}

.breadcrumb {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.breadcrumb a {
  color: var(--primary-color);
  text-decoration: none;
}

.breadcrumb .current {
  color: var(--text-secondary);
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 32px;
  align-items: start;
}

.detail-main {}

/* Cover */
.cover-section {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  aspect-ratio: 16/9;
  margin-bottom: 24px;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 50%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
}

.cover-meta {
  display: flex;
  gap: 10px;
  align-items: center;
}

.cover-meta > * {
  background: rgba(0,0,0,0.5);
  color: #fff;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.78rem;
}

.start-learn-btn {
  align-self: center;
  padding: 14px 40px;
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 16px rgba(66, 184, 131, 0.5);
}

.start-learn-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(66, 184, 131, 0.6);
}

/* Header */
.tutorial-header {
  margin-bottom: 32px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.category-tag {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.78rem;
  color: #fff;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: transparent;
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
}

.action-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.action-btn.collected {
  border-color: #e74c3c;
  color: #e74c3c;
}

.tutorial-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.tutorial-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 0.88rem;
  color: var(--text-secondary);
}

.stars {
  letter-spacing: 2px;
  color: #f39c12;
}

.tutorial-desc {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 12px;
}

.tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* Chapters */
.chapters-section {}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chapter-progress {
  font-size: 0.8rem;
  font-weight: 400;
  color: var(--text-muted);
}

.chapters-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chapter-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.chapter-item:hover {
  border-color: var(--primary-color);
  background: rgba(66, 184, 131, 0.03);
}

.chapter-item.completed {
  border-color: rgba(39, 174, 96, 0.3);
}

.chapter-item.locked {
  opacity: 0.6;
  cursor: not-allowed;
}

.chapter-number {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.chapter-item.completed .chapter-number {
  background: rgba(39, 174, 96, 0.1);
  color: var(--color-success);
}

.chapter-info {
  flex: 1;
}

.chapter-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.chapter-meta {
  display: flex;
  gap: 8px;
  font-size: 0.78rem;
  color: var(--text-muted);
}

.free-tag {
  background: rgba(39, 174, 96, 0.1);
  color: var(--color-success);
  padding: 1px 8px;
  border-radius: 4px;
}

.lock-tag {
  background: rgba(243, 156, 18, 0.1);
  color: var(--color-warning);
  padding: 1px 8px;
  border-radius: 4px;
}

.chapter-play {
  padding: 6px 14px;
  border: 1px solid var(--primary-color);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--primary-color);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.chapter-play:hover {
  background: var(--primary-color);
  color: #fff;
}

/* Sidebar */
.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 80px;
}

.author-card,
.info-card,
.progress-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
}

.author-card {
  display: flex;
  align-items: center;
  gap: 14px;
}

.author-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  color: #fff;
  font-weight: 700;
  flex-shrink: 0;
}

.author-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
}

.author-title {
  font-size: 0.78rem;
  color: var(--text-muted);
}

.info-card h3,
.progress-card h3 {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 14px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.info-label {
  color: var(--text-muted);
}

.info-value {
  font-weight: 600;
  color: var(--text-primary);
}

.progress-bar-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: var(--bg-soft);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-color-light));
  border-radius: 4px;
  transition: width 0.5s;
}

.progress-text {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--primary-color);
  width: 40px;
  text-align: right;
}

.progress-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
}

@media (max-width: 1024px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
  .detail-sidebar {
    position: static;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .detail-sidebar {
    grid-template-columns: 1fr;
  }
}
</style>
