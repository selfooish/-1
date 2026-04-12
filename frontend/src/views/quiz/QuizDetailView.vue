<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG } from '@/utils'

const route = useRoute()
const router = useRouter()
const quizStore = useQuizStore()

const quizId = computed(() => Number(route.params.id))
const quiz = computed(() => quizStore.currentQuiz)
const questions = computed(() => quizStore.questions)
const loading = computed(() => quizStore.loading)

const rules = computed(() => {
  if (!quiz.value) return []
  return [
    `共 ${quiz.value.questionCount} 道题`,
    `限时 ${quiz.value.timeLimit} 分钟`,
    `满分 ${quiz.value.totalScore} 分，${quiz.value.passScore} 分及格`,
    '提交后会立即显示当前得分和每题情况',
  ]
})

onMounted(() => {
  if (quizId.value) {
    quizStore.fetchQuizDetail(quizId.value)
  }
})
</script>

<template>
  <div class="page-shell">
    <div class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/quizzes">在线答题</RouterLink>
      <span>/</span>
      <span>{{ quiz?.title || '答题详情' }}</span>
    </div>

    <div v-if="loading" class="state-card">正在加载答题详情...</div>

    <div v-else-if="quiz" class="detail-grid">
      <section class="main-panel">
        <div class="hero-card">
          <div class="tag-row">
            <span class="pill" :style="{ background: CATEGORY_CONFIG[quiz.category]?.color || '#64748b' }">
              {{ CATEGORY_CONFIG[quiz.category]?.label || quiz.category }}
            </span>
            <span
              class="pill pill-light"
              :style="{
                color: DIFFICULTY_CONFIG[quiz.difficulty]?.color,
                background: DIFFICULTY_CONFIG[quiz.difficulty]?.bgColor,
              }"
            >
              {{ DIFFICULTY_CONFIG[quiz.difficulty]?.label }}
            </span>
          </div>

          <h1 class="page-title">{{ quiz.title }}</h1>
          <p class="desc">{{ quiz.description }}</p>

          <div class="meta-row">
            <span>已加载题目 {{ questions.length }} 道</span>
            <span>作答 {{ quiz.attemptCount }} 次</span>
            <span v-if="quiz.bestScore !== undefined">最高分 {{ quiz.bestScore }}</span>
          </div>
        </div>

        <div class="section-card">
          <h2>答题说明</h2>
          <ul class="list">
            <li v-for="rule in rules" :key="rule">{{ rule }}</li>
          </ul>
        </div>
      </section>

      <aside class="side-panel">
        <div class="section-card">
          <h3>开始作答</h3>
          <div class="info-list">
            <div class="info-item">
              <span>题目数</span>
              <strong>{{ quiz.questionCount }}</strong>
            </div>
            <div class="info-item">
              <span>限时</span>
              <strong>{{ quiz.timeLimit }} 分钟</strong>
            </div>
            <div class="info-item">
              <span>及格线</span>
              <strong>{{ quiz.passScore }}</strong>
            </div>
          </div>

          <button class="btn btn-primary full-btn" @click="router.push(`/quizzes/${quiz.id}/do`)">
            开始答题
          </button>
        </div>
      </aside>
    </div>

    <div v-else class="state-card">没有找到对应答题。</div>
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
}

.main-panel,
.side-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hero-card,
.section-card,
.state-card {
  padding: 20px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.tag-row,
.meta-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.tag-row {
  margin-bottom: 12px;
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

.page-title {
  margin: 0 0 10px;
  color: var(--text-primary);
  font-size: 30px;
}

.desc {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.7;
}

.meta-row {
  margin-top: 16px;
  color: var(--text-muted);
}

.list {
  margin: 0;
  padding-left: 18px;
  color: var(--text-secondary);
  line-height: 1.8;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 16px 0 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.full-btn {
  width: 100%;
}

.state-card {
  text-align: center;
  color: var(--text-muted);
}

@media (max-width: 960px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
