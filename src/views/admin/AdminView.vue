<script setup lang="ts">
import { ref } from 'vue'

const activeAdminTab = ref('tutorials')

const adminStats = ref([
  { label: '用户总数', value: 1284, icon: '👥', color: '#3498db' },
  { label: '教程数量', value: 86, icon: '🎬', color: '#42b883' },
  { label: '题目总数', value: 2340, icon: '📝', color: '#e67e22' },
  { label: '待审核任务', value: 12, icon: '⏳', color: '#e74c3c' },
])

const pendingTasks = ref([
  { id: 1, user: '张三', task: '电饭煲清洁维护', submittedAt: '2025-01-22', points: 50 },
  { id: 2, user: '李四', task: '绿萝养护记录', submittedAt: '2025-01-21', points: 80 },
  { id: 3, user: '王五', task: '家庭安全自查', submittedAt: '2025-01-21', points: 70 },
])

const recentUsers = ref([
  { id: 1, nickname: '小红', username: 'xiaohong', role: 'student', points: 450, joinedAt: '2025-01-20' },
  { id: 2, nickname: '小强', username: 'xiaoqiang', role: 'student', points: 230, joinedAt: '2025-01-19' },
  { id: 3, nickname: '小芳', username: 'xiaofang', role: 'teacher', points: 1200, joinedAt: '2025-01-18' },
])

function approveTask(id: number) {
  pendingTasks.value = pendingTasks.value.filter(t => t.id !== id)
}
</script>

<template>
  <div class="admin-view">
    <div class="admin-header">
      <h1>🛠️ CMS 管理后台</h1>
      <p>管理教程内容、审核实践任务、维护用户数据</p>
    </div>

    <!-- 数据概览 -->
    <div class="admin-stats">
      <div v-for="stat in adminStats" :key="stat.label" class="admin-stat-card" :style="{ '--stat-color': stat.color }">
        <span class="stat-icon">{{ stat.icon }}</span>
        <div>
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <!-- 管理标签 -->
    <div class="admin-tabs">
      <button
        v-for="tab in [
          { key: 'tutorials', label: '📚 教程管理' },
          { key: 'quizzes', label: '📝 题目管理' },
          { key: 'tasks', label: '🎯 任务审核' },
          { key: 'users', label: '👥 用户管理' },
        ]"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeAdminTab === tab.key }"
        @click="activeAdminTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 任务审核 -->
    <div v-if="activeAdminTab === 'tasks'" class="admin-panel">
      <div class="panel-header">
        <h3>待审核任务 ({{ pendingTasks.length }})</h3>
      </div>
      <div class="admin-table">
        <div class="table-header">
          <span>提交用户</span>
          <span>任务名称</span>
          <span>提交时间</span>
          <span>积分</span>
          <span>操作</span>
        </div>
        <div v-for="task in pendingTasks" :key="task.id" class="table-row">
          <span>{{ task.user }}</span>
          <span>{{ task.task }}</span>
          <span>{{ task.submittedAt }}</span>
          <span class="points-cell">+{{ task.points }}</span>
          <div class="action-btns">
            <button class="btn btn-sm btn-primary" @click="approveTask(task.id)">通过</button>
            <button class="btn btn-sm btn-outline" @click="() => {}">详情</button>
          </div>
        </div>
        <div v-if="pendingTasks.length === 0" class="empty-row">
          <span>🎉 当前没有待审核任务</span>
        </div>
      </div>
    </div>

    <!-- 用户管理 -->
    <div v-if="activeAdminTab === 'users'" class="admin-panel">
      <div class="panel-header">
        <h3>最近注册用户</h3>
      </div>
      <div class="admin-table">
        <div class="table-header">
          <span>昵称</span>
          <span>用户名</span>
          <span>角色</span>
          <span>积分</span>
          <span>注册时间</span>
        </div>
        <div v-for="user in recentUsers" :key="user.id" class="table-row">
          <span>{{ user.nickname }}</span>
          <span class="mono-text">{{ user.username }}</span>
          <span>
            <span class="role-badge" :class="user.role">
              {{ user.role === 'admin' ? '管理员' : user.role === 'teacher' ? '教师' : '学生' }}
            </span>
          </span>
          <span class="points-cell">⭐ {{ user.points }}</span>
          <span>{{ user.joinedAt }}</span>
        </div>
      </div>
    </div>

    <!-- 教程管理 -->
    <div v-if="activeAdminTab === 'tutorials'" class="admin-panel">
      <div class="panel-header">
        <h3>教程管理</h3>
        <button class="btn btn-primary btn-sm">+ 添加教程</button>
      </div>
      <div class="admin-table">
        <div class="table-header">
          <span>教程名称</span>
          <span>分类</span>
          <span>难度</span>
          <span>观看量</span>
          <span>操作</span>
        </div>
        <div v-for="t in [{id:1,title:'电饭煲维修',cat:'家电维修',diff:'进阶',views:2341},{id:2,title:'衣柜收纳',cat:'收纳整理',diff:'入门',views:4102}]" :key="t.id" class="table-row">
          <span>{{ t.title }}</span>
          <span>{{ t.cat }}</span>
          <span><span class="difficulty-badge">{{ t.diff }}</span></span>
          <span>{{ t.views }}</span>
          <div class="action-btns">
            <button class="btn btn-sm btn-outline">编辑</button>
            <button class="btn btn-sm btn-outline" style="color:var(--color-danger)">删除</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 题目管理 -->
    <div v-if="activeAdminTab === 'quizzes'" class="admin-panel">
      <div class="panel-header">
        <h3>题库管理</h3>
        <button class="btn btn-primary btn-sm">+ 添加题目</button>
      </div>
      <div class="admin-table">
        <div class="table-header">
          <span>题目内容</span>
          <span>类型</span>
          <span>分类</span>
          <span>难度</span>
          <span>操作</span>
        </div>
        <div v-for="q in [{id:1,stem:'电饭煲不通电应先检查...',type:'单选题',cat:'家电维修',diff:'入门'},{id:2,stem:'以下哪些方法可延长绿萝...',type:'多选题',cat:'绿植养护',diff:'进阶'}]" :key="q.id" class="table-row">
          <span class="stem-text">{{ q.stem }}</span>
          <span>{{ q.type }}</span>
          <span>{{ q.cat }}</span>
          <span><span class="difficulty-badge">{{ q.diff }}</span></span>
          <div class="action-btns">
            <button class="btn btn-sm btn-outline">编辑</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-view {}

.admin-header {
  margin-bottom: 28px;
}

.admin-header h1 {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.admin-header p {
  font-size: 0.88rem;
  color: var(--text-muted);
}

.admin-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.admin-stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.stat-icon {
  font-size: 2rem;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 900;
  color: var(--stat-color);
  line-height: 1;
}

.stat-label {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.admin-tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 24px;
}

.tab-btn {
  padding: 10px 18px;
  border: none;
  background: transparent;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-muted);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  margin-bottom: -1px;
}

.tab-btn.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
}

.admin-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}

.panel-header h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
}

.admin-table {
  width: 100%;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 0.8fr 0.8fr 1.2fr;
  gap: 12px;
  padding: 10px 20px;
  background: var(--bg-soft);
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 0.8fr 0.8fr 1.2fr;
  gap: 12px;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border-color);
  font-size: 0.85rem;
  color: var(--text-primary);
  align-items: center;
  transition: background 0.2s;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background: var(--bg-soft);
}

.points-cell {
  color: var(--primary-color);
  font-weight: 700;
}

.mono-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
}

.role-badge {
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 600;
}

.role-badge.admin {
  background: rgba(231, 76, 60, 0.1);
  color: var(--color-danger);
}

.role-badge.teacher {
  background: rgba(52, 152, 219, 0.1);
  color: var(--color-info);
}

.role-badge.student {
  background: rgba(66, 184, 131, 0.1);
  color: var(--primary-color);
}

.difficulty-badge {
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 600;
  background: var(--bg-soft);
  color: var(--text-secondary);
}

.action-btns {
  display: flex;
  gap: 6px;
}

.stem-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-row {
  padding: 32px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.88rem;
}

@media (max-width: 1024px) {
  .admin-stats { grid-template-columns: repeat(2, 1fr); }
  .table-header, .table-row { grid-template-columns: 2fr 1fr 1fr 1fr; }
  .table-header span:nth-child(4), .table-row span:nth-child(4) { display: none; }
}
</style>
