<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG } from '@/utils'

const taskStore = useTaskStore()

const tasks = computed(() => taskStore.taskList)
const loading = computed(() => taskStore.loading)

onMounted(() => {
  taskStore.fetchTaskList()
})
</script>

<template>
  <div class="page-shell">
    <div class="page-header">
      <div>
        <p class="eyebrow">Tasks</p>
        <h1 class="page-title">实践任务</h1>
        <p class="page-desc">任务列表已经改为从 FastAPI `/tasks` 拉取。</p>
      </div>
      <RouterLink to="/my-tasks" class="btn btn-outline">查看我的任务</RouterLink>
    </div>

    <div v-if="loading" class="state-card">正在加载任务...</div>

    <div v-else-if="tasks.length" class="task-grid">
      <RouterLink
        v-for="task in tasks"
        :key="task.id"
        :to="`/tasks/${task.id}`"
        class="task-card"
      >
        <img :src="task.coverImage" :alt="task.title" class="task-cover" />
        <div class="task-body">
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
          <h3 class="task-title">{{ task.title }}</h3>
          <p class="task-desc">{{ task.description }}</p>
          <div class="task-meta">
            <span>积分 {{ task.points }}</span>
            <span>截止 {{ task.deadline.slice(0, 10) }}</span>
          </div>
        </div>
      </RouterLink>
    </div>

    <div v-else class="state-card">当前没有任务数据。</div>
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

.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}

.task-card,
.state-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.task-card {
  overflow: hidden;
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.task-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.task-cover {
  width: 100%;
  height: 170px;
  object-fit: cover;
  display: block;
}

.task-body {
  padding: 16px;
}

.tag-row,
.task-meta {
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

.task-title {
  margin: 0 0 10px;
  color: var(--text-primary);
  font-size: 18px;
  line-height: 1.4;
}

.task-desc {
  margin: 0 0 14px;
  color: var(--text-muted);
  line-height: 1.6;
}

.task-meta {
  color: var(--text-secondary);
  font-size: 14px;
}

.state-card {
  padding: 48px 20px;
  text-align: center;
  color: var(--text-muted);
}
</style>
