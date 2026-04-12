<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG } from '@/utils'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()

const taskId = computed(() => Number(route.params.id))
const task = computed(() => taskStore.currentTask)
const loading = computed(() => taskStore.loading)

const requirements = [
  '提交一段实践过程说明，建议写清楚操作步骤。',
  '至少上传 1 个成果附件，图片或视频都可以。',
  '内容尽量体现你自己的理解和实践过程。',
]

const evaluation = [
  '是否完整完成任务目标。',
  '是否能清楚展示实践过程。',
  '提交内容是否真实、清晰、有条理。',
]

onMounted(() => {
  if (taskId.value) {
    taskStore.fetchTaskDetail(taskId.value)
  }
})
</script>

<template>
  <div class="page-shell">
    <div class="breadcrumb">
      <RouterLink to="/">首页</RouterLink>
      <span>/</span>
      <RouterLink to="/tasks">实践任务</RouterLink>
      <span>/</span>
      <span>{{ task?.title || '任务详情' }}</span>
    </div>

    <div v-if="loading" class="state-card">正在加载任务详情...</div>

    <div v-else-if="task" class="detail-grid">
      <section class="main-panel">
        <img :src="task.coverImage" :alt="task.title" class="hero-cover" />

        <div class="section-card">
          <div class="tag-row">
            <span class="pill" :style="{ background: CATEGORY_CONFIG[task.category]?.color || '#64748b' }">
              {{ CATEGORY_CONFIG[task.category]?.label || task.category }}
            </span>
            <span
              class="pill pill-light"
              :style="{
                color: DIFFICULTY_CONFIG[task.difficulty]?.color,
                background: DIFFICULTY_CONFIG[task.difficulty]?.bgColor,
              }"
            >
              {{ DIFFICULTY_CONFIG[task.difficulty]?.label }}
            </span>
          </div>

          <h1 class="page-title">{{ task.title }}</h1>
          <p class="desc">{{ task.description }}</p>

          <div class="meta-row">
            <span>积分 {{ task.points }}</span>
            <span>截止 {{ task.deadline.slice(0, 10) }}</span>
            <span>已提交 {{ task.submitCount }}/{{ task.maxSubmits }}</span>
            <span>状态 {{ task.status }}</span>
          </div>
        </div>

        <div class="section-card">
          <h2>提交要求</h2>
          <ul class="list">
            <li v-for="item in requirements" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="section-card">
          <h2>评估标准</h2>
          <ul class="list">
            <li v-for="item in evaluation" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div v-if="task.reviewerComment" class="section-card">
          <h2>评语反馈</h2>
          <p class="desc">{{ task.reviewerComment }}</p>
        </div>
      </section>

      <aside class="side-panel">
        <div class="section-card">
          <h3>任务操作</h3>
          <div class="info-list">
            <div class="info-item">
              <span>当前状态</span>
              <strong>{{ task.status }}</strong>
            </div>
            <div class="info-item">
              <span>审核结果</span>
              <strong>{{ task.reviewStatus || '待审核' }}</strong>
            </div>
          </div>

          <button class="btn btn-primary full-btn" @click="router.push(`/tasks/${task.id}/submit`)">
            去提交成果
          </button>
          <RouterLink to="/tasks" class="back-link">返回任务列表</RouterLink>
        </div>
      </aside>
    </div>

    <div v-else class="state-card">没有找到对应任务。</div>
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

.hero-cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.section-card,
.state-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.section-card {
  padding: 20px;
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

.back-link {
  display: inline-block;
  margin-top: 12px;
  color: var(--text-muted);
  text-decoration: none;
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
