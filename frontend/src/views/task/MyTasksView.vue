<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useTaskStore } from '@/stores/task'

const taskStore = useTaskStore()

const tasks = computed(() => taskStore.myTasks)
const loading = computed(() => taskStore.loading)

const statusLabelMap: Record<string, string> = {
  pending: '待开始',
  in_progress: '进行中',
  submitted: '待审核',
  reviewed: '已完成',
}

onMounted(() => {
  taskStore.fetchMyTasks()
})
</script>

<template>
  <div class="page-shell">
    <div class="page-header">
      <div>
        <p class="eyebrow">My Tasks</p>
        <h1 class="page-title">我的任务</h1>
        <p class="page-desc">这里展示当前登录用户从 FastAPI `/tasks/my` 获取到的任务状态。</p>
      </div>
      <RouterLink to="/tasks" class="btn btn-primary">去任务广场</RouterLink>
    </div>

    <div v-if="loading" class="state-card">正在加载我的任务...</div>

    <div v-else-if="tasks.length" class="task-list">
      <div v-for="task in tasks" :key="task.id" class="task-row">
        <div class="task-main">
          <RouterLink :to="`/tasks/${task.id}`" class="task-title">{{ task.title }}</RouterLink>
          <div class="task-meta">
            <span>截止 {{ task.deadline.slice(0, 10) }}</span>
            <span>积分 {{ task.points }}</span>
            <span>已提交 {{ task.submitCount }}/{{ task.maxSubmits }}</span>
          </div>
          <p v-if="task.reviewerComment" class="review-comment">{{ task.reviewerComment }}</p>
        </div>
        <div class="task-side">
          <span class="status-badge">{{ statusLabelMap[task.status] || task.status }}</span>
          <RouterLink :to="`/tasks/${task.id}/submit`" class="btn btn-outline btn-sm">
            提交成果
          </RouterLink>
        </div>
      </div>
    </div>

    <div v-else class="state-card">你还没有任务记录。</div>
  </div>
</template>

<style scoped>
.page-shell {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
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

.task-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.task-row,
.state-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.task-row {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  padding: 20px;
}

.task-main {
  flex: 1;
}

.task-title {
  color: var(--text-primary);
  text-decoration: none;
  font-size: 18px;
  font-weight: 700;
}

.task-title:hover {
  color: var(--primary-color);
}

.task-meta {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 10px;
  color: var(--text-muted);
  font-size: 14px;
}

.review-comment {
  margin: 12px 0 0;
  padding: 12px;
  border-radius: var(--radius-md);
  background: var(--bg-soft);
  color: var(--text-secondary);
}

.task-side {
  display: flex;
  flex-direction: column;
  align-items: end;
  gap: 12px;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(66, 184, 131, 0.1);
  color: var(--primary-color);
  font-size: 13px;
  font-weight: 700;
}

.state-card {
  padding: 48px 20px;
  text-align: center;
  color: var(--text-muted);
}

@media (max-width: 720px) {
  .task-row,
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .task-side {
    align-items: start;
  }
}
</style>
