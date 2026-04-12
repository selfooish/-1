<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useTutorialStore } from '@/stores/tutorial'
import { useTaskStore } from '@/stores/task'
import { useQuizStore } from '@/stores/quiz'
import { useUserStore } from '@/stores/user'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG, getAvatarBg } from '@/utils'

const tutorialStore = useTutorialStore()
const taskStore = useTaskStore()
const quizStore = useQuizStore()
const userStore = useUserStore()

const bannerIndex = ref(0)
let bannerTimer: ReturnType<typeof setInterval> | null = null

const featuredTutorials = computed(() => tutorialStore.tutorials.slice(0, 4))
const featuredTasks = computed(() => taskStore.taskList.slice(0, 3))
const featuredQuizzes = computed(() => quizStore.quizList.slice(0, 3))
const categories = computed(() => Object.entries(CATEGORY_CONFIG).slice(0, 8))

const stats = computed(() => [
  { label: '教程总数', value: tutorialStore.total || tutorialStore.tutorials.length, hint: '来自 /tutorials' },
  { label: '任务总数', value: taskStore.taskList.length, hint: '来自 /tasks' },
  { label: '题库数量', value: quizStore.quizList.length, hint: '来自 /quizzes' },
  { label: '我的积分', value: userStore.userInfo?.points || 0, hint: '来自 /user/profile' },
])

function rotateBanner() {
  bannerIndex.value = (bannerIndex.value + 1) % 3
}

async function loadHomeData() {
  await Promise.all([
    tutorialStore.fetchTutorials({ page: 1, pageSize: 4 }),
    taskStore.fetchTaskList({ page: 1 }),
    quizStore.fetchQuizList({ page: 1 }),
    userStore.isLoggedIn ? userStore.fetchUserInfo() : Promise.resolve(),
  ])
}

onMounted(async () => {
  await loadHomeData()
  bannerTimer = setInterval(rotateBanner, 5000)
})

onBeforeUnmount(() => {
  if (bannerTimer) clearInterval(bannerTimer)
})
</script>

<template>
  <div class="home-shell">
    <section class="hero-banner">
      <div class="banner-track" :style="{ transform: `translateX(-${bannerIndex * 100}%)` }">
        <div class="hero-slide slide-a">
          <div class="hero-copy">
            <p class="eyebrow">Labor Platform</p>
            <h1>前后端已经分离，首页数据现在直接来自 FastAPI。</h1>
            <p>教程、任务、题库和个人积分都会在这里动态展示，方便你后续继续扩展真实业务。</p>
            <div class="hero-actions">
              <RouterLink to="/tutorials" class="btn btn-primary btn-lg">进入教程</RouterLink>
              <RouterLink to="/tasks" class="btn btn-outline btn-lg">查看任务</RouterLink>
            </div>
          </div>
        </div>

        <div class="hero-slide slide-b">
          <div class="hero-copy">
            <p class="eyebrow">Practice</p>
            <h1>任务提交、题库作答、学习进度已经能串起来。</h1>
            <p>你后面只要把 mock 数据逐步换成数据库查询，这套前端就能继续往上接。</p>
            <div class="hero-actions">
              <RouterLink to="/quizzes" class="btn btn-primary btn-lg">开始答题</RouterLink>
              <RouterLink to="/growth" class="btn btn-outline btn-lg">查看成长</RouterLink>
            </div>
          </div>
        </div>

        <div class="hero-slide slide-c">
          <div class="hero-copy">
            <p class="eyebrow">Admin</p>
            <h1>后台页也可以拿真实统计和待审核任务了。</h1>
            <p>现在已经具备一个很适合继续往数据库和后台管理扩展的前端基础。</p>
            <div class="hero-actions">
              <RouterLink to="/admin" class="btn btn-primary btn-lg">进入后台</RouterLink>
              <RouterLink to="/profile" class="btn btn-outline btn-lg">个人中心</RouterLink>
            </div>
          </div>
        </div>
      </div>

      <div class="banner-dots">
        <button
          v-for="index in 3"
          :key="index"
          class="dot"
          :class="{ active: bannerIndex === index - 1 }"
          @click="bannerIndex = index - 1"
        />
      </div>
    </section>

    <section class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card">
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-label">{{ stat.label }}</div>
        <div class="stat-hint">{{ stat.hint }}</div>
      </div>
    </section>

    <section class="panel-section">
      <div class="section-header">
        <h2>技能分类</h2>
        <RouterLink to="/tutorials" class="section-link">查看全部</RouterLink>
      </div>

      <div class="category-grid">
        <RouterLink
          v-for="[key, category] in categories"
          :key="key"
          :to="`/tutorials?category=${encodeURIComponent(key)}`"
          class="category-card"
          :style="{ borderColor: category.color }"
        >
          <div class="category-name">{{ category.label }}</div>
          <div class="category-desc">{{ category.description }}</div>
        </RouterLink>
      </div>
    </section>

    <section class="panel-section">
      <div class="section-header">
        <h2>精选教程</h2>
        <RouterLink to="/tutorials" class="section-link">查看全部</RouterLink>
      </div>

      <div class="content-grid">
        <RouterLink
          v-for="tutorial in featuredTutorials"
          :key="tutorial.id"
          :to="`/tutorials/${tutorial.id}`"
          class="content-card"
        >
          <img :src="tutorial.coverImage" :alt="tutorial.title" class="content-cover" />
          <div class="content-body">
            <div class="tag-row">
              <span class="pill" :style="{ background: CATEGORY_CONFIG[tutorial.category]?.color || '#64748b' }">
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
            <h3>{{ tutorial.title }}</h3>
            <p>{{ tutorial.description }}</p>
            <div class="footer-row">
              <span class="author">
                <span class="avatar" :style="{ background: getAvatarBg(tutorial.author) }">
                  {{ tutorial.author?.[0] || 'A' }}
                </span>
                {{ tutorial.author }}
              </span>
              <span>{{ tutorial.viewCount }} 浏览</span>
            </div>
          </div>
        </RouterLink>
      </div>
    </section>

    <section class="split-grid">
      <div class="panel-section compact-section">
        <div class="section-header">
          <h2>最新任务</h2>
          <RouterLink to="/tasks" class="section-link">更多任务</RouterLink>
        </div>
        <div class="mini-list">
          <RouterLink
            v-for="task in featuredTasks"
            :key="task.id"
            :to="`/tasks/${task.id}`"
            class="mini-item"
          >
            <strong>{{ task.title }}</strong>
            <span>{{ task.points }} 积分</span>
          </RouterLink>
        </div>
      </div>

      <div class="panel-section compact-section">
        <div class="section-header">
          <h2>题库挑战</h2>
          <RouterLink to="/quizzes" class="section-link">更多题库</RouterLink>
        </div>
        <div class="mini-list">
          <RouterLink
            v-for="quiz in featuredQuizzes"
            :key="quiz.id"
            :to="`/quizzes/${quiz.id}`"
            class="mini-item"
          >
            <strong>{{ quiz.title }}</strong>
            <span>{{ quiz.questionCount }} 题 / {{ quiz.timeLimit }} 分钟</span>
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-shell {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.hero-banner {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
}

.banner-track {
  display: flex;
  transition: transform 0.5s ease;
}

.hero-slide {
  min-width: 100%;
  min-height: 360px;
  display: flex;
  align-items: center;
  padding: 40px;
}

.slide-a {
  background: linear-gradient(135deg, #1f4b3f, #2f7b60);
}

.slide-b {
  background: linear-gradient(135deg, #173b66, #2460a3);
}

.slide-c {
  background: linear-gradient(135deg, #5f3a19, #b4681c);
}

.hero-copy {
  max-width: 640px;
  color: #fff;
}

.eyebrow {
  margin: 0 0 10px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.8;
}

.hero-copy h1 {
  margin: 0 0 14px;
  font-size: 40px;
  line-height: 1.2;
}

.hero-copy p {
  margin: 0;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 24px;
}

.banner-dots {
  position: absolute;
  left: 50%;
  bottom: 18px;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
  cursor: pointer;
}

.dot.active {
  background: #fff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card,
.panel-section {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.stat-card {
  padding: 20px;
}

.stat-value {
  font-size: 30px;
  font-weight: 800;
  color: var(--primary-color);
}

.stat-label {
  margin-top: 8px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-hint {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 13px;
}

.panel-section {
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-header h2 {
  margin: 0;
  font-size: 22px;
  color: var(--text-primary);
}

.section-link {
  color: var(--primary-color);
  text-decoration: none;
}

.category-grid,
.content-grid,
.split-grid {
  display: grid;
  gap: 16px;
}

.category-grid {
  grid-template-columns: repeat(4, 1fr);
}

.category-card {
  padding: 18px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  text-decoration: none;
  background: var(--bg-base);
}

.category-name {
  font-weight: 700;
  color: var(--text-primary);
}

.category-desc {
  margin-top: 8px;
  color: var(--text-muted);
  line-height: 1.6;
  font-size: 14px;
}

.content-grid {
  grid-template-columns: repeat(4, 1fr);
}

.content-card {
  overflow: hidden;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-base);
  text-decoration: none;
}

.content-cover {
  width: 100%;
  height: 170px;
  object-fit: cover;
  display: block;
}

.content-body {
  padding: 16px;
}

.content-body h3 {
  margin: 0 0 8px;
  color: var(--text-primary);
  font-size: 18px;
}

.content-body p {
  margin: 0 0 14px;
  color: var(--text-muted);
  line-height: 1.6;
}

.tag-row,
.footer-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag-row {
  margin-bottom: 12px;
}

.footer-row {
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
  font-size: 14px;
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

.author {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}

.split-grid {
  grid-template-columns: 1fr 1fr;
}

.mini-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.mini-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-base);
  text-decoration: none;
  color: var(--text-secondary);
}

.mini-item strong {
  color: var(--text-primary);
}

@media (max-width: 1100px) {
  .stats-grid,
  .category-grid,
  .content-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 760px) {
  .hero-slide {
    padding: 28px;
    min-height: 320px;
  }

  .hero-copy h1 {
    font-size: 30px;
  }

  .stats-grid,
  .category-grid,
  .content-grid,
  .split-grid {
    grid-template-columns: 1fr;
  }
}
</style>
