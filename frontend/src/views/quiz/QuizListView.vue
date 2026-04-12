<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG } from '@/utils'

const quizStore = useQuizStore()

const quizzes = computed(() => quizStore.quizList)
const loading = computed(() => quizStore.loading)

onMounted(() => {
  quizStore.fetchQuizList()
})
</script>

<template>
  <div class="page-shell">
    <div class="page-header">
      <div>
        <p class="eyebrow">Quizzes</p>
        <h1 class="page-title">在线答题</h1>
        <p class="page-desc">题库列表已经接到 FastAPI `/quizzes`。</p>
      </div>
    </div>

    <div v-if="loading" class="state-card">正在加载题库...</div>

    <div v-else-if="quizzes.length" class="quiz-grid">
      <RouterLink
        v-for="quiz in quizzes"
        :key="quiz.id"
        :to="`/quizzes/${quiz.id}`"
        class="quiz-card"
      >
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

        <h3 class="quiz-title">{{ quiz.title }}</h3>
        <p class="quiz-desc">{{ quiz.description }}</p>

        <div class="quiz-meta">
          <span>{{ quiz.questionCount }} 题</span>
          <span>{{ quiz.timeLimit }} 分钟</span>
          <span>及格 {{ quiz.passScore }}</span>
        </div>

        <div class="quiz-record">
          <span>作答 {{ quiz.attemptCount }} 次</span>
          <span v-if="quiz.bestScore !== undefined">最高分 {{ quiz.bestScore }}</span>
        </div>
      </RouterLink>
    </div>

    <div v-else class="state-card">当前没有题库数据。</div>
  </div>
</template>

<style scoped>
.page-shell {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--primary-color);
}

.page-title {
  margin: 0;
  color: var(--text-primary);
  font-size: 32px;
  font-weight: 800;
}

.page-desc {
  margin: 8px 0 0;
  color: var(--text-muted);
}

.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}

.quiz-card,
.state-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.quiz-card {
  padding: 18px;
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.quiz-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.tag-row,
.quiz-meta,
.quiz-record {
  display: flex;
  gap: 8px;
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

.quiz-title {
  margin: 0 0 10px;
  color: var(--text-primary);
  font-size: 18px;
}

.quiz-desc {
  margin: 0 0 14px;
  color: var(--text-muted);
  line-height: 1.6;
}

.quiz-meta,
.quiz-record {
  color: var(--text-secondary);
  font-size: 14px;
}

.quiz-record {
  margin-top: 10px;
}

.state-card {
  padding: 48px 20px;
  text-align: center;
  color: var(--text-muted);
}
</style>
