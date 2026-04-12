<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/request'
import type { Quiz, Task, TaskSubmission, Tutorial, User } from '@/types'

type AdminStats = {
  userCount: number
  tutorialCount: number
  quizCount: number
  pendingTaskSubmissionCount: number
  quizRecordCount: number
  taskCount: number
}

type AdminSubmission = TaskSubmission & {
  user: User
  task: Task
}

const activeTab = ref<'overview' | 'tasks' | 'users' | 'tutorials' | 'quizzes'>('overview')
const loading = ref(false)

const stats = ref<AdminStats | null>(null)
const users = ref<User[]>([])
const pendingSubmissions = ref<AdminSubmission[]>([])
const tutorials = ref<Tutorial[]>([])
const quizzes = ref<Quiz[]>([])

async function loadAdminData() {
  loading.value = true
  try {
    const [statsRes, usersRes, submissionsRes, tutorialsRes, quizzesRes] = await Promise.all([
      api.get<AdminStats>('/admin/stats'),
      api.get<User[]>('/admin/users'),
      api.get<AdminSubmission[]>('/admin/tasks/submissions/pending'),
      api.get<{ list: Tutorial[] }>('/tutorials', { params: { page: 1, pageSize: 20 } }),
      api.get<{ list: Quiz[] }>('/quizzes', { params: { page: 1 } }),
    ])

    stats.value = statsRes.data
    users.value = usersRes.data
    pendingSubmissions.value = submissionsRes.data
    tutorials.value = tutorialsRes.data.list
    quizzes.value = quizzesRes.data.list
  } finally {
    loading.value = false
  }
}

async function approveSubmission(submissionId: number) {
  try {
    await api.post(`/admin/tasks/submissions/${submissionId}/approve`)
    ElMessage.success('审核通过')
    await loadAdminData()
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '审核失败')
  }
}

const overviewCards = computed(() => [
  { label: '用户总数', value: stats.value?.userCount || 0 },
  { label: '教程数量', value: stats.value?.tutorialCount || 0 },
  { label: '题库数量', value: stats.value?.quizCount || 0 },
  { label: '待审核提交', value: stats.value?.pendingTaskSubmissionCount || 0 },
  { label: '任务总数', value: stats.value?.taskCount || 0 },
  { label: '答题记录', value: stats.value?.quizRecordCount || 0 },
])

onMounted(loadAdminData)
</script>

<template>
  <div class="admin-shell">
    <div class="page-header">
      <div>
        <p class="eyebrow">Admin</p>
        <h1>后台管理</h1>
        <p>现在使用真实接口加载统计、用户列表、待审核任务、教程列表和题库列表。</p>
      </div>
      <button class="btn btn-outline" :disabled="loading" @click="loadAdminData">
        {{ loading ? '刷新中...' : '刷新数据' }}
      </button>
    </div>

    <div class="tabs">
      <button class="tab-btn" :class="{ active: activeTab === 'overview' }" @click="activeTab = 'overview'">
        概览
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'tasks' }" @click="activeTab = 'tasks'">
        待审核任务
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'users' }" @click="activeTab = 'users'">
        用户
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'tutorials' }" @click="activeTab = 'tutorials'">
        教程
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'quizzes' }" @click="activeTab = 'quizzes'">
        题库
      </button>
    </div>

    <section v-if="activeTab === 'overview'" class="stats-grid">
      <div v-for="card in overviewCards" :key="card.label" class="stat-card">
        <div class="stat-value">{{ card.value }}</div>
        <div class="stat-label">{{ card.label }}</div>
      </div>
    </section>

    <section v-else-if="activeTab === 'tasks'" class="panel-card">
      <div class="panel-header">
        <h2>待审核任务提交</h2>
        <span>{{ pendingSubmissions.length }} 条</span>
      </div>
      <div class="table-list">
        <div v-for="submission in pendingSubmissions" :key="submission.id" class="table-row">
          <div class="row-main">
            <strong>{{ submission.task.title }}</strong>
            <div class="row-meta">
              <span>用户 {{ submission.user.nickname }}</span>
              <span>提交时间 {{ submission.submittedAt.slice(0, 10) }}</span>
              <span>建议积分 {{ submission.task.points }}</span>
            </div>
          </div>
          <button class="btn btn-primary btn-sm" @click="approveSubmission(submission.id)">审核通过</button>
        </div>
        <div v-if="!pendingSubmissions.length" class="empty-state">当前没有待审核任务。</div>
      </div>
    </section>

    <section v-else-if="activeTab === 'users'" class="panel-card">
      <div class="panel-header">
        <h2>用户列表</h2>
        <span>{{ users.length }} 个</span>
      </div>
      <div class="table-list">
        <div v-for="user in users" :key="user.id" class="table-row">
          <div class="row-main">
            <strong>{{ user.nickname }}</strong>
            <div class="row-meta">
              <span>{{ user.username }}</span>
              <span>{{ user.role }}</span>
              <span>{{ user.points }} 积分</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section v-else-if="activeTab === 'tutorials'" class="panel-card">
      <div class="panel-header">
        <h2>教程列表</h2>
        <span>{{ tutorials.length }} 条</span>
      </div>
      <div class="table-list">
        <div v-for="tutorial in tutorials" :key="tutorial.id" class="table-row">
          <div class="row-main">
            <strong>{{ tutorial.title }}</strong>
            <div class="row-meta">
              <span>{{ tutorial.category }}</span>
              <span>{{ tutorial.difficulty }}</span>
              <span>{{ tutorial.viewCount }} 浏览</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section v-else class="panel-card">
      <div class="panel-header">
        <h2>题库列表</h2>
        <span>{{ quizzes.length }} 条</span>
      </div>
      <div class="table-list">
        <div v-for="quiz in quizzes" :key="quiz.id" class="table-row">
          <div class="row-main">
            <strong>{{ quiz.title }}</strong>
            <div class="row-meta">
              <span>{{ quiz.category }}</span>
              <span>{{ quiz.questionCount }} 题</span>
              <span>{{ quiz.passScore }} 分及格</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.admin-shell {
  display: flex;
  flex-direction: column;
  gap: 24px;
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

.page-header h1 {
  margin: 0;
  font-size: 32px;
  color: var(--text-primary);
}

.page-header p {
  margin: 8px 0 0;
  color: var(--text-muted);
}

.tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 18px;
  border-radius: 999px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-secondary);
  cursor: pointer;
}

.tab-btn.active {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-card,
.panel-card {
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
  color: var(--text-primary);
  font-weight: 700;
}

.panel-card {
  padding: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.panel-header h2 {
  margin: 0;
  font-size: 22px;
  color: var(--text-primary);
}

.panel-header span {
  color: var(--text-muted);
}

.table-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.table-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-base);
}

.row-main strong {
  color: var(--text-primary);
}

.row-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 8px;
  color: var(--text-muted);
  font-size: 14px;
}

.empty-state {
  padding: 28px;
  text-align: center;
  color: var(--text-muted);
}

@media (max-width: 960px) {
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .table-row,
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
