<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { DIFFICULTY_CONFIG, CATEGORY_CONFIG } from '@/utils'

const quizList = ref([
  { id: 1, title: '家电维修基础知识测验', description: '考察电饭煲、电风扇等常见家电的故障判断与维修基础', category: '家电维修', difficulty: 'easy' as const, questionCount: 15, timeLimit: 20, passScore: 60, attemptCount: 3, bestScore: 85, tags: ['家电维修', '基础知识'] },
  { id: 2, title: '收纳整理能力考核', description: '测试你对衣柜、厨房、书桌等空间收纳方法的理解', category: '收纳整理', difficulty: 'easy' as const, questionCount: 10, timeLimit: 15, passScore: 60, attemptCount: 2, bestScore: 95, tags: ['收纳', '空间管理'] },
  { id: 3, title: '绿植养护综合测试', description: '涵盖常见绿植的浇水、施肥、光照、繁殖等知识点', category: '绿植养护', difficulty: 'medium' as const, questionCount: 20, timeLimit: 30, passScore: 70, attemptCount: 1, bestScore: 78, tags: ['绿植', '养护', '综合'] },
  { id: 4, title: '家庭手工技能测验', description: '考察布艺、纸艺、环保手工等手工制作的基础知识', category: '手工制作', difficulty: 'easy' as const, questionCount: 12, timeLimit: 18, passScore: 60, attemptCount: 0, bestScore: undefined, tags: ['手工', 'DIY'] },
  { id: 5, title: '家庭安全知识竞赛', description: '消防、用电、防溺水、食品药品安全等综合安全知识', category: '安全常识', difficulty: 'medium' as const, questionCount: 25, timeLimit: 35, passScore: 75, attemptCount: 0, bestScore: undefined, tags: ['安全', '综合', '竞赛'] },
  { id: 6, title: '衣物护理与熨烫考核', description: '考察衣物材质识别、洗涤方式、熨烫温度等知识', category: '衣物护理', difficulty: 'medium' as const, questionCount: 15, timeLimit: 20, passScore: 65, attemptCount: 0, bestScore: undefined, tags: ['衣物', '熨烫', '护理'] },
  { id: 7, title: '厨房清洁卫生测试', description: '测试厨房各区域清洁技巧与卫生防护知识', category: '清洁卫生', difficulty: 'easy' as const, questionCount: 10, timeLimit: 15, passScore: 60, attemptCount: 0, bestScore: undefined, tags: ['清洁', '卫生', '厨房'] },
  { id: 8, title: '综合劳动知识挑战赛', description: '涵盖所有劳动技能分类的综合能力测试，挑战满分！', category: '综合', difficulty: 'hard' as const, questionCount: 40, timeLimit: 60, passScore: 80, attemptCount: 0, bestScore: undefined, tags: ['综合', '挑战', '满分'] },
])
</script>

<template>
  <div class="quiz-list-view">
    <div class="page-header">
      <h1 class="page-title"><span>📝</span> 在线答题</h1>
      <p class="page-desc">检验学习成果，巩固劳动技能知识。每次测验都有时间限制哦！</p>
    </div>

    <div class="quiz-grid">
      <RouterLink
        v-for="quiz in quizList"
        :key="quiz.id"
        :to="`/quizzes/${quiz.id}`"
        class="quiz-card"
      >
        <div class="quiz-header">
          <span class="quiz-category" :style="{ background: CATEGORY_CONFIG[quiz.category]?.color || '#888' }">
            {{ CATEGORY_CONFIG[quiz.category]?.icon }} {{ quiz.category }}
          </span>
          <span class="quiz-difficulty"
            :style="{ background: DIFFICULTY_CONFIG[quiz.difficulty]?.bgColor, color: DIFFICULTY_CONFIG[quiz.difficulty]?.color }">
            {{ DIFFICULTY_CONFIG[quiz.difficulty]?.label }}
          </span>
        </div>
        <h3 class="quiz-title">{{ quiz.title }}</h3>
        <p class="quiz-desc">{{ quiz.description }}</p>
        <div class="quiz-tags">
          <span v-for="tag in quiz.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
        <div class="quiz-meta">
          <span>📋 {{ quiz.questionCount }} 题</span>
          <span>⏱ {{ quiz.timeLimit }} 分钟</span>
          <span>🎯 {{ quiz.passScore }}% 及格</span>
        </div>
        <div class="quiz-footer">
          <div v-if="quiz.bestScore !== undefined" class="quiz-record">
            <span class="best-score">🏆 最高分: {{ quiz.bestScore }}分</span>
            <span class="attempt-count">已做 {{ quiz.attemptCount }} 次</span>
          </div>
          <div v-else class="quiz-record">
            <span class="not-attempted">📝 还未作答</span>
          </div>
          <button class="quiz-action-btn">
            {{ quiz.bestScore !== undefined ? '重新答题' : '开始答题' }} →
          </button>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.quiz-list-view {}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-desc {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.quiz-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.quiz-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
  text-decoration: none;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quiz-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-color);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quiz-category {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  color: #fff;
  font-weight: 600;
}

.quiz-difficulty {
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
}

.quiz-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
}

.quiz-desc {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.quiz-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.quiz-meta {
  display: flex;
  gap: 12px;
  font-size: 0.78rem;
  color: var(--text-secondary);
}

.quiz-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
  margin-top: 4px;
}

.best-score {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--color-warning);
}

.attempt-count {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-left: 8px;
}

.not-attempted {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.quiz-action-btn {
  padding: 6px 14px;
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.quiz-action-btn:hover {
  background: var(--primary-color-dark);
}

@media (max-width: 1024px) {
  .quiz-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .quiz-grid { grid-template-columns: 1fr; }
}
</style>
