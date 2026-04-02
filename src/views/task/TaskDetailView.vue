<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG } from '@/utils'

const route = useRoute()
const router = useRouter()
const taskId = Number(route.params.id)

const task = ref({
  id: taskId,
  title: '完成一次电饭煲清洁与维护',
  description: '将家中电饭煲拆解清洗，并记录清洁前后对比照片。电饭煲是家庭中经常使用的电器，内部容易积累污垢和水垢，定期清洁不仅能延长使用寿命，还能保证食品安全。',
  category: '家电维修',
  coverImage: 'https://picsum.photos/seed/task1/800/400',
  points: 50,
  difficulty: 'easy' as const,
  deadline: '2025-02-28',
  submitCount: 0,
  maxSubmits: 1,
  requirements: [
    '拍摄清洁前的电饭煲外观照片',
    '记录清洁过程（至少3张）',
    '拍摄清洁后的电饭煲照片',
    '撰写50字以上的清洁心得',
    '上传所有照片（jpg/png格式）',
  ],
  evaluation: [
    '照片清晰完整（40分）',
    '过程记录详细（30分）',
    '清洁心得有感悟（30分）',
  ],
  tips: '建议使用白醋或小苏打溶液清洁水垢，效果更好！',
})
</script>

<template>
  <div class="task-detail-view">
    <div class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span> / </span>
      <RouterLink to="/tasks">实践任务</RouterLink>
      <span> / </span>
      <span>{{ task.title }}</span>
    </div>

    <div class="detail-grid">
      <div class="detail-main">
        <div class="task-cover">
          <img :src="task.coverImage" :alt="task.title" />
          <div class="cover-badges">
            <span class="task-points">+{{ task.points }} 积分</span>
            <span class="task-difficulty"
              :style="{ background: DIFFICULTY_CONFIG[task.difficulty]?.bgColor, color: DIFFICULTY_CONFIG[task.difficulty]?.color }">
              {{ DIFFICULTY_CONFIG[task.difficulty]?.label }}
            </span>
            <span class="task-category"
              :style="{ background: CATEGORY_CONFIG[task.category]?.color }">
              {{ CATEGORY_CONFIG[task.category]?.icon }} {{ task.category }}
            </span>
          </div>
        </div>

        <div class="task-header">
          <h1 class="task-title">{{ task.title }}</h1>
          <div class="task-meta">
            <span>📅 截止日期：{{ task.deadline }}</span>
            <span>📤 已提交 {{ task.submitCount }} 人</span>
          </div>
        </div>

        <div class="task-section">
          <h3>任务描述</h3>
          <p>{{ task.description }}</p>
        </div>

        <div class="task-section">
          <h3>📋 提交要求</h3>
          <ul class="requirements-list">
            <li v-for="req in task.requirements" :key="req">
              <span class="req-icon">✅</span> {{ req }}
            </li>
          </ul>
        </div>

        <div class="task-section">
          <h3>📊 评分标准</h3>
          <ul class="requirements-list">
            <li v-for="ev in task.evaluation" :key="ev">
              <span class="req-icon">⭐</span> {{ ev }}
            </li>
          </ul>
        </div>

        <div class="task-tip">
          <span>💡 小贴士：</span> {{ task.tips }}
        </div>
      </div>

      <aside class="detail-sidebar">
        <div class="submit-card">
          <div class="points-display">
            <div class="points-value">+{{ task.points }}</div>
            <div class="points-label">积分奖励</div>
          </div>
          <div class="submit-info">
            <div class="info-item">
              <span>📅 截止日期</span>
              <strong>{{ task.deadline }}</strong>
            </div>
            <div class="info-item">
              <span>👥 已参与</span>
              <strong>{{ task.submitCount }} 人</strong>
            </div>
            <div class="info-item">
              <span>📤 提交次数</span>
              <strong>{{ task.submitCount }}/{{ task.maxSubmits }}</strong>
            </div>
          </div>
          <button class="btn btn-primary btn-lg" style="width:100%;margin-top:16px"
            @click="router.push(`/tasks/${taskId}/submit`)">
            📤 提交成果
          </button>
          <RouterLink to="/tasks" class="back-link">← 返回任务列表</RouterLink>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.breadcrumb { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 24px; }
.breadcrumb a { color: var(--primary-color); text-decoration: none; }
.detail-grid { display: grid; grid-template-columns: 1fr 320px; gap: 32px; align-items: start; }
.task-cover { position: relative; border-radius: var(--radius-lg); overflow: hidden; aspect-ratio: 16/9; margin-bottom: 24px; }
.task-cover img { width: 100%; height: 100%; object-fit: cover; }
.cover-badges { position: absolute; top: 12px; left: 12px; right: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
.task-points { background: rgba(66,184,131,0.9); color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
.task-difficulty { padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; }
.task-category { padding: 3px 10px; border-radius: 4px; font-size: 0.72rem; color: #fff; font-weight: 600; }
.task-header { margin-bottom: 24px; }
.task-title { font-size: 1.6rem; font-weight: 800; color: var(--text-primary); margin-bottom: 10px; }
.task-meta { display: flex; gap: 16px; font-size: 0.82rem; color: var(--text-muted); }
.task-section { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 20px; margin-bottom: 16px; }
.task-section h3 { font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 14px; }
.task-section p { font-size: 0.88rem; color: var(--text-secondary); line-height: 1.7; }
.requirements-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.requirements-list li { display: flex; align-items: flex-start; gap: 10px; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; }
.req-icon { flex-shrink: 0; }
.task-tip { background: rgba(66,184,131,0.06); border: 1px solid rgba(66,184,131,0.2); border-radius: var(--radius-lg); padding: 16px 20px; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6; }
.task-tip span { font-weight: 700; color: var(--primary-color); }
.detail-sidebar { position: sticky; top: 80px; }
.submit-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 24px; }
.points-display { text-align: center; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid var(--border-color); }
.points-value { font-size: 3rem; font-weight: 900; color: var(--primary-color); line-height: 1; }
.points-label { font-size: 0.82rem; color: var(--text-muted); margin-top: 4px; }
.submit-info { display: flex; flex-direction: column; gap: 10px; }
.info-item { display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted); }
.info-item strong { color: var(--text-primary); }
.back-link { display: block; margin-top: 12px; font-size: 0.82rem; color: var(--text-muted); text-decoration: none; text-align: center; transition: color 0.2s; }
.back-link:hover { color: var(--primary-color); }
@media (max-width: 1024px) { .detail-grid { grid-template-columns: 1fr; } .detail-sidebar { position: static; } }
</style>
