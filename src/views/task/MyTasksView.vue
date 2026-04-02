<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const myTasks = ref([
  { id: 1, title: '完成一次电饭煲清洁与维护', category: '家电维修', points: 50, deadline: '2025-02-28', status: 'submitted' as const, submittedAt: '2025-01-15', reviewStatus: 'excellent' as const, reviewerComment: '照片清晰，过程记录详细，非常棒！' },
  { id: 3, title: '养护一株绿萝并记录成长', category: '绿植养护', points: 80, deadline: '2025-04-01', status: 'in_progress' as const, submittedAt: '', reviewStatus: undefined as any, reviewerComment: '' },
  { id: 5, title: '家庭安全自查：排查用电隐患', category: '安全常识', points: 70, deadline: '2025-03-10', status: 'pending' as const, submittedAt: '', reviewStatus: undefined as any, reviewerComment: '' },
  { id: 7, title: '熨烫衣物练习：整理衬衫', category: '衣物护理', points: 40, deadline: '2025-02-10', status: 'reviewed' as const, submittedAt: '2025-02-08', reviewStatus: 'pass' as const, reviewerComment: '基本掌握熨烫技巧，继续加油！' },
])
</script>

<template>
  <div class="my-tasks-view">
    <div class="page-header">
      <h1 class="page-title"><span>📋</span> 我的任务</h1>
      <RouterLink to="/tasks" class="btn btn-primary">🎯 领取新任务</RouterLink>
    </div>

    <div class="task-list">
      <div v-for="task in myTasks" :key="task.id" class="task-item">
        <div class="task-item-left">
          <div class="task-status-dot" :class="task.status" />
          <div class="task-item-info">
            <RouterLink :to="`/tasks/${task.id}`" class="task-item-title">{{ task.title }}</RouterLink>
            <div class="task-item-meta">
              <span class="task-category">{{ task.category }}</span>
              <span>📅 {{ task.deadline }}</span>
              <span>⭐ {{ task.points }} 积分</span>
            </div>
          </div>
        </div>
        <div class="task-item-right">
          <span class="status-badge" :class="task.status">
            {{ task.status === 'pending' ? '未领取' : task.status === 'in_progress' ? '进行中' : task.status === 'submitted' ? '待审核' : '已完成' }}
          </span>
          <template v-if="task.status === 'submitted' && task.reviewStatus">
            <span class="review-badge" :class="task.reviewStatus">
              {{ task.reviewStatus === 'excellent' ? '🏆 优秀' : task.reviewStatus === 'pass' ? '✅ 及格' : '❌ 不及格' }}
            </span>
          </template>
          <RouterLink v-if="task.status === 'in_progress'" :to="`/tasks/${task.id}/submit`" class="btn btn-sm btn-primary">
            📤 提交
          </RouterLink>
          <RouterLink v-if="task.status === 'pending'" :to="`/tasks/${task.id}`" class="btn btn-sm btn-outline">
            领取
          </RouterLink>
        </div>
        <div v-if="task.reviewerComment" class="reviewer-comment">
          评委点评：{{ task.reviewerComment }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
.page-title { font-size: 1.8rem; font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 10px; }
.task-list { display: flex; flex-direction: column; gap: 12px; }
.task-item { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 20px 24px; display: flex; flex-direction: column; gap: 12px; transition: box-shadow 0.2s; }
.task-item:hover { box-shadow: var(--shadow-md); }
.task-item-left { display: flex; align-items: flex-start; gap: 14px; }
.task-status-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; margin-top: 5px; }
.task-status-dot.pending { background: var(--text-muted); }
.task-status-dot.in_progress { background: var(--color-warning); }
.task-status-dot.submitted { background: var(--color-info); }
.task-status-dot.reviewed { background: var(--color-success); }
.task-item-title { font-size: 0.95rem; font-weight: 700; color: var(--text-primary); text-decoration: none; transition: color 0.2s; }
.task-item-title:hover { color: var(--primary-color); }
.task-item-meta { display: flex; gap: 12px; font-size: 0.78rem; color: var(--text-muted); margin-top: 6px; }
.task-category { background: var(--primary-bg); color: var(--primary-color); padding: 1px 8px; border-radius: 4px; font-weight: 600; }
.task-item-right { display: flex; align-items: center; gap: 10px; margin-left: 24px; }
.status-badge { padding: 3px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.status-badge.pending { background: rgba(136,150,166,0.1); color: var(--text-muted); }
.status-badge.in_progress { background: rgba(243,156,18,0.1); color: var(--color-warning); }
.status-badge.submitted { background: rgba(52,152,219,0.1); color: var(--color-info); }
.status-badge.reviewed { background: rgba(39,174,96,0.1); color: var(--color-success); }
.review-badge { padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.review-badge.excellent { background: rgba(243,156,18,0.1); color: var(--color-warning); }
.review-badge.pass { background: rgba(39,174,96,0.1); color: var(--color-success); }
.review-badge.fail { background: rgba(231,76,60,0.1); color: var(--color-danger); }
.reviewer-comment { margin-left: 24px; font-size: 0.82rem; color: var(--text-secondary); padding: 10px 14px; background: rgba(0,0,0,0.03); border-radius: var(--radius-md); border-left: 3px solid var(--primary-color); }
</style>
