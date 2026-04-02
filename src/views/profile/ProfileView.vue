<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { getLevelFromPoints, getAvatarBg } from '@/utils'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const activeTab = ref('overview')

const userData = ref({
  nickname: userStore.userInfo?.nickname || '小明',
  username: userStore.userInfo?.username || 'xiaoming',
  email: 'xiaoming@example.com',
  phone: '138****8888',
  bio: '热爱劳动，喜欢动手实践，正在学习各种生活技能！',
  joinedAt: '2024-09-01',
})

const learningStats = ref([
  { label: '已完成教程', value: 12, icon: '🎬', color: '#42b883' },
  { label: '完成测验', value: 8, icon: '📝', color: '#3498db' },
  { label: '完成任务', value: 5, icon: '🎯', color: '#e67e22' },
  { label: '获得勋章', value: 6, icon: '🏅', color: '#9b59b6' },
])

const recentActivities = ref([
  { id: 1, type: 'tutorial', text: '完成了教程《电饭煲维修》', time: '2小时前' },
  { id: 2, type: 'quiz', text: '答题《家电维修测验》获得85分', time: '1天前' },
  { id: 3, type: 'task', text: '提交任务「电饭煲清洁」', time: '2天前' },
  { id: 4, type: 'badge', text: '获得「答题达人」勋章', time: '3天前' },
])

function saveProfile() {
  ElMessage.success('个人信息已保存')
}

const levelInfo = getLevelFromPoints(850)
</script>

<template>
  <div class="profile-view">
    <div class="profile-header">
      <div class="profile-avatar-wrap">
        <div class="profile-avatar" :style="{ background: getAvatarBg(userData.nickname) }">
          {{ userData.nickname[0] }}
        </div>
        <div class="profile-level-badge">Lv.{{ levelInfo.level }}</div>
      </div>
      <div class="profile-info">
        <h1>{{ userData.nickname }}</h1>
        <p class="profile-title">{{ levelInfo.title }}</p>
        <p class="profile-bio">{{ userData.bio }}</p>
        <div class="profile-meta">
          <span>📅 加入于 {{ userData.joinedAt }}</span>
          <span>⭐ 850 积分</span>
        </div>
      </div>
      <div class="profile-stats">
        <div v-for="stat in learningStats" :key="stat.label" class="stat-item" :style="{ '--stat-color': stat.color }">
          <span class="stat-icon">{{ stat.icon }}</span>
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </div>

    <div class="profile-tabs">
      <button
        v-for="tab in [{ key: 'overview', label: '学习概览' }, { key: 'settings', label: '个人设置' }]"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <div v-if="activeTab === 'overview'" class="profile-content">
      <div class="content-grid">
        <div class="card">
          <h3>最近活动</h3>
          <div class="activity-list">
            <div v-for="act in recentActivities" :key="act.id" class="activity-item">
              <span class="activity-icon">
                {{ act.type === 'tutorial' ? '🎬' : act.type === 'quiz' ? '📝' : act.type === 'task' ? '🎯' : '🏅' }}
              </span>
              <span class="activity-text">{{ act.text }}</span>
              <span class="activity-time">{{ act.time }}</span>
            </div>
          </div>
        </div>

        <div class="card">
          <h3>我的收藏</h3>
          <div class="favorites-empty">
            <div class="empty-icon">❤️</div>
            <p>暂无收藏，浏览教程时点击收藏按钮即可收藏</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="profile-content">
      <div class="card settings-card">
        <h3>个人信息</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>昵称</label>
            <input v-model="userData.nickname" class="form-input" />
          </div>
          <div class="form-group">
            <label>用户名</label>
            <input v-model="userData.username" class="form-input" disabled />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="userData.email" type="email" class="form-input" />
          </div>
          <div class="form-group">
            <label>手机号</label>
            <input v-model="userData.phone" class="form-input" />
          </div>
          <div class="form-group full-width">
            <label>个人简介</label>
            <textarea v-model="userData.bio" class="form-textarea" rows="3" />
          </div>
        </div>
        <button class="btn btn-primary" style="margin-top:20px" @click="saveProfile">保存修改</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-view {}

.profile-header {
  background: linear-gradient(135deg, #1a4a2e, #2d7a4e);
  border-radius: var(--radius-xl);
  padding: 32px;
  margin-bottom: 24px;
  display: flex;
  gap: 28px;
  align-items: flex-start;
}

.profile-avatar-wrap {
  position: relative;
  flex-shrink: 0;
}

.profile-avatar {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.4rem;
  color: #fff;
  font-weight: 800;
  border: 4px solid rgba(255,255,255,0.3);
}

.profile-level-badge {
  position: absolute;
  bottom: -6px;
  right: -6px;
  background: #ffd700;
  color: #fff;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 10px;
  border: 2px solid #fff;
}

.profile-info {
  flex: 1;
  color: #fff;
}

.profile-info h1 {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 4px;
}

.profile-title {
  font-size: 0.88rem;
  opacity: 0.8;
  margin-bottom: 8px;
}

.profile-bio {
  font-size: 0.85rem;
  opacity: 0.75;
  line-height: 1.6;
  margin-bottom: 10px;
}

.profile-meta {
  display: flex;
  gap: 16px;
  font-size: 0.78rem;
  opacity: 0.7;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  flex-shrink: 0;
}

.stat-item {
  background: rgba(255,255,255,0.1);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  text-align: center;
  backdrop-filter: blur(4px);
}

.stat-icon {
  font-size: 1.4rem;
  display: block;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 1.4rem;
  font-weight: 900;
  color: var(--stat-color);
  display: block;
}

.stat-label {
  font-size: 0.68rem;
  color: rgba(255,255,255,0.7);
}

.profile-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background: transparent;
  font-size: 0.9rem;
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

.tab-btn:hover {
  color: var(--text-primary);
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
}

.card h3 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 14px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
}

.activity-icon {
  width: 28px;
  height: 28px;
  background: var(--bg-soft);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  flex-shrink: 0;
}

.activity-text {
  flex: 1;
  color: var(--text-primary);
}

.activity-time {
  color: var(--text-muted);
  font-size: 0.72rem;
  flex-shrink: 0;
}

.favorites-empty {
  text-align: center;
  padding: 30px;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 8px;
}

.favorites-empty p {
  font-size: 0.85rem;
}

.settings-card {
  max-width: 640px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
}

.form-input {
  padding: 10px 14px;
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.88rem;
  color: var(--text-primary);
  background: var(--bg-base);
  outline: none;
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-input:focus {
  border-color: var(--primary-color);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-textarea {
  padding: 10px 14px;
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.88rem;
  color: var(--text-primary);
  background: var(--bg-base);
  outline: none;
  resize: vertical;
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-textarea:focus {
  border-color: var(--primary-color);
}

@media (max-width: 768px) {
  .profile-header { flex-direction: column; }
  .profile-stats { grid-template-columns: repeat(4, 1fr); width: 100%; }
  .content-grid { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
}
</style>
