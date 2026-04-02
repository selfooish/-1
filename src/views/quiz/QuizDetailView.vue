<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG } from '@/utils'

const route = useRoute()
const router = useRouter()
const quizId = Number(route.params.id)

const quiz = ref({
  id: quizId,
  title: '家电维修基础知识测验',
  description: '考察电饭煲、电风扇等常见家电的故障判断与维修基础，帮助你检验学习成果。',
  category: '家电维修',
  difficulty: 'easy' as const,
  questionCount: 15,
  timeLimit: 20,
  passScore: 60,
  totalScore: 100,
  attemptCount: 3,
  bestScore: 85,
  tags: ['家电维修', '基础知识'],
  rules: [
    '共 15 道题，含单选题、多选题、判断题',
    '答题时间 20 分钟，超时自动提交',
    '及格分数 60 分（满分 100）',
    '允许重复作答，每次作答独立计分',
  ],
})
</script>

<template>
  <div class="quiz-detail-view">
    <div class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span> / </span>
      <RouterLink to="/quizzes">在线答题</RouterLink>
      <span> / </span>
      <span>{{ quiz.title }}</span>
    </div>

    <div class="detail-grid">
      <div class="detail-main">
        <div class="quiz-hero">
          <div class="quiz-hero-icon">📝</div>
          <div>
            <div class="quiz-hero-tags">
              <span class="quiz-category" :style="{ background: CATEGORY_CONFIG[quiz.category]?.color }">
                {{ CATEGORY_CONFIG[quiz.category]?.icon }} {{ quiz.category }}
              </span>
              <span class="quiz-difficulty"
                :style="{ background: DIFFICULTY_CONFIG[quiz.difficulty]?.bgColor, color: DIFFICULTY_CONFIG[quiz.difficulty]?.color }">
                {{ DIFFICULTY_CONFIG[quiz.difficulty]?.label }}
              </span>
            </div>
            <h1 class="quiz-title">{{ quiz.title }}</h1>
            <p class="quiz-desc">{{ quiz.description }}</p>
          </div>
        </div>

        <div class="quiz-rules-card">
          <h3>📋 测验须知</h3>
          <ul>
            <li v-for="rule in quiz.rules" :key="rule">{{ rule }}</li>
          </ul>
        </div>

        <div class="quiz-scores">
          <div v-if="quiz.bestScore !== undefined" class="best-score-card">
            <div class="best-label">🏆 历史最高分</div>
            <div class="best-value">{{ quiz.bestScore }}</div>
            <div class="best-append">分</div>
          </div>
          <div class="attempt-info">
            已作答 {{ quiz.attemptCount }} 次
          </div>
        </div>
      </div>

      <aside class="detail-sidebar">
        <div class="quiz-info-card">
          <h3>测验信息</h3>
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">题目数量</span>
              <span class="info-value">{{ quiz.questionCount }} 题</span>
            </div>
            <div class="info-item">
              <span class="info-label">时间限制</span>
              <span class="info-value">{{ quiz.timeLimit }} 分钟</span>
            </div>
            <div class="info-item">
              <span class="info-label">及格分数</span>
              <span class="info-value">{{ quiz.passScore }} 分</span>
            </div>
            <div class="info-item">
              <span class="info-label">总分</span>
              <span class="info-value">{{ quiz.totalScore }} 分</span>
            </div>
            <div class="info-item">
              <span class="info-label">难度</span>
              <span class="info-value" :style="{ color: DIFFICULTY_CONFIG[quiz.difficulty]?.color }">
                {{ DIFFICULTY_CONFIG[quiz.difficulty]?.label }}
              </span>
            </div>
          </div>
        </div>

        <div class="action-card">
          <button class="btn btn-primary btn-lg" style="width:100%" @click="router.push(`/quizzes/${quizId}/do`)">
            {{ quiz.bestScore !== undefined ? '🔄 重新答题' : '📝 开始答题' }}
          </button>
          <RouterLink to="/quizzes" class="back-link">← 返回题库</RouterLink>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.quiz-detail-view {}

.breadcrumb {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.breadcrumb a {
  color: var(--primary-color);
  text-decoration: none;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 32px;
  align-items: start;
}

.quiz-hero {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 24px;
}

.quiz-hero-icon {
  font-size: 3.5rem;
  flex-shrink: 0;
}

.quiz-hero-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.quiz-category {
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  color: #fff;
  font-weight: 600;
}

.quiz-difficulty {
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
}

.quiz-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.quiz-desc {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.7;
}

.quiz-rules-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 24px;
}

.quiz-rules-card h3 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 14px;
}

.quiz-rules-card ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quiz-rules-card li {
  font-size: 0.88rem;
  color: var(--text-secondary);
  padding-left: 20px;
  position: relative;
}

.quiz-rules-card li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--primary-color);
}

.quiz-scores {
  display: flex;
  gap: 20px;
  align-items: center;
}

.best-score-card {
  background: linear-gradient(135deg, rgba(243, 156, 18, 0.08), rgba(243, 156, 18, 0.04));
  border: 1px solid rgba(243, 156, 18, 0.2);
  border-radius: var(--radius-lg);
  padding: 20px 28px;
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.best-label {
  font-size: 0.8rem;
  color: var(--color-warning);
  margin-right: 8px;
}

.best-value {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-warning);
  line-height: 1;
}

.best-append {
  font-size: 1rem;
  color: var(--color-warning);
  font-weight: 600;
}

.attempt-info {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 80px;
}

.quiz-info-card,
.action-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
}

.quiz-info-card h3,
.action-card h3 {
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

.action-card {
  text-align: center;
}

.back-link {
  display: block;
  margin-top: 12px;
  font-size: 0.82rem;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--primary-color);
}

@media (max-width: 1024px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
  .detail-sidebar {
    position: static;
  }
}
</style>
