<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { useGrowthStore } from '@/stores/growth'
import { getAvatarBg } from '@/utils'

const userStore = useUserStore()
const growthStore = useGrowthStore()

const activeTab = ref<'overview' | 'settings'>('overview')
const saving = ref(false)

const profileForm = reactive({
  nickname: '',
  email: '',
  phone: '',
  bio: '',
})

const user = computed(() => userStore.userInfo)
const levelInfo = computed(() => userStore.levelInfo)
const pointRecords = computed(() => growthStore.pointRecords)
const unlockedBadgeCount = computed(() => growthStore.unlockedBadges.length)

const learningStats = computed(() => [
  {
    label: '教程积分记录',
    value: pointRecords.value.filter((item) => item.type === 'tutorial').length,
  },
  {
    label: '答题积分记录',
    value: pointRecords.value.filter((item) => item.type === 'quiz').length,
  },
  {
    label: '任务积分记录',
    value: pointRecords.value.filter((item) => item.type === 'task').length,
  },
  {
    label: '已获得徽章',
    value: unlockedBadgeCount.value,
  },
])

const recentActivities = computed(() => pointRecords.value.slice(0, 6))

watch(
  user,
  (value) => {
    if (!value) return
    profileForm.nickname = value.nickname || ''
    profileForm.email = value.email || ''
    profileForm.phone = value.phone || ''
    profileForm.bio = value.bio || ''
  },
  { immediate: true }
)

async function loadProfileData() {
  await Promise.all([userStore.fetchUserInfo(), growthStore.fetchPointRecords(), growthStore.fetchBadges()])
}

async function saveProfile() {
  saving.value = true
  try {
    await userStore.updateProfile({
      nickname: profileForm.nickname,
      email: profileForm.email,
      phone: profileForm.phone,
      bio: profileForm.bio,
    })
    ElMessage.success('个人资料已保存')
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(loadProfileData)
</script>

<template>
  <div class="profile-shell">
    <div class="hero-card">
      <div class="avatar-block">
        <div class="avatar" :style="{ background: getAvatarBg(user?.nickname || 'U') }">
          {{ user?.nickname?.[0] || 'U' }}
        </div>
        <span class="level-badge">Lv.{{ levelInfo?.level || 1 }}</span>
      </div>

      <div class="hero-main">
        <h1>{{ user?.nickname || '未登录用户' }}</h1>
        <div class="hero-subtitle">{{ levelInfo?.title || '学习者' }}</div>
        <p>{{ user?.bio || '这里显示从 /user/profile 拉取的个人简介。' }}</p>
        <div class="meta-row">
          <span>用户名 {{ user?.username }}</span>
          <span>积分 {{ user?.points || 0 }}</span>
          <span>加入时间 {{ user?.createdAt?.slice(0, 10) }}</span>
        </div>
      </div>

      <div class="hero-stats">
        <div v-for="item in learningStats" :key="item.label" class="stat-chip">
          <strong>{{ item.value }}</strong>
          <span>{{ item.label }}</span>
        </div>
      </div>
    </div>

    <div class="tabs">
      <button class="tab-btn" :class="{ active: activeTab === 'overview' }" @click="activeTab = 'overview'">
        学习概览
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'settings' }" @click="activeTab = 'settings'">
        个人设置
      </button>
    </div>

    <div v-if="activeTab === 'overview'" class="overview-grid">
      <section class="panel-card">
        <div class="panel-header">
          <h2>最近活动</h2>
          <span>{{ recentActivities.length }} 条</span>
        </div>
        <div class="activity-list">
          <div v-for="record in recentActivities" :key="record.id" class="activity-item">
            <div>
              <div class="activity-title">{{ record.action }}</div>
              <div class="activity-time">{{ record.createdAt.slice(0, 10) }}</div>
            </div>
            <strong class="activity-points">+{{ record.points }}</strong>
          </div>
        </div>
      </section>

      <section class="panel-card">
        <div class="panel-header">
          <h2>账号信息</h2>
        </div>
        <div class="info-list">
          <div class="info-item">
            <span>邮箱</span>
            <strong>{{ user?.email || '未填写' }}</strong>
          </div>
          <div class="info-item">
            <span>手机</span>
            <strong>{{ user?.phone || '未填写' }}</strong>
          </div>
          <div class="info-item">
            <span>徽章数量</span>
            <strong>{{ unlockedBadgeCount }}</strong>
          </div>
        </div>
      </section>
    </div>

    <section v-else class="panel-card settings-card">
      <div class="panel-header">
        <h2>编辑资料</h2>
        <span>保存到 /user/profile</span>
      </div>

      <div class="form-grid">
        <label class="form-group">
          <span>昵称</span>
          <input v-model="profileForm.nickname" class="form-input" />
        </label>
        <label class="form-group">
          <span>邮箱</span>
          <input v-model="profileForm.email" class="form-input" type="email" />
        </label>
        <label class="form-group">
          <span>手机</span>
          <input v-model="profileForm.phone" class="form-input" />
        </label>
        <label class="form-group full-width">
          <span>简介</span>
          <textarea v-model="profileForm.bio" class="form-textarea" rows="5" />
        </label>
      </div>

      <button class="btn btn-primary" :disabled="saving" @click="saveProfile">
        {{ saving ? '保存中...' : '保存修改' }}
      </button>
    </section>
  </div>
</template>

<style scoped>
.profile-shell {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero-card {
  display: flex;
  gap: 24px;
  padding: 28px 32px;
  border-radius: var(--radius-xl);
  background: linear-gradient(135deg, #1d4d44, #2e7762);
  color: #fff;
}

.avatar-block {
  position: relative;
}

.avatar {
  width: 92px;
  height: 92px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
  font-weight: 800;
  color: #fff;
  border: 4px solid rgba(255, 255, 255, 0.2);
}

.level-badge {
  position: absolute;
  right: -6px;
  bottom: -6px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #f59e0b;
  color: #fff;
  font-size: 12px;
  font-weight: 800;
}

.hero-main {
  flex: 1;
}

.hero-main h1 {
  margin: 0;
  font-size: 32px;
}

.hero-subtitle {
  margin-top: 8px;
  font-weight: 700;
  opacity: 0.85;
}

.hero-main p {
  margin: 12px 0 0;
  line-height: 1.7;
  opacity: 0.9;
}

.meta-row {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 14px;
  font-size: 14px;
  opacity: 0.85;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  min-width: 240px;
}

.stat-chip,
.panel-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.stat-chip {
  padding: 14px;
  background: rgba(255, 255, 255, 0.12);
}

.stat-chip strong {
  display: block;
  font-size: 24px;
}

.stat-chip span {
  display: block;
  margin-top: 6px;
  font-size: 13px;
}

.tabs {
  display: flex;
  gap: 10px;
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

.overview-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 16px;
}

.panel-card {
  padding: 20px;
  background: var(--bg-card);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.panel-header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 22px;
}

.panel-header span {
  color: var(--text-muted);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-base);
}

.activity-title {
  color: var(--text-primary);
  font-weight: 700;
}

.activity-time {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 14px;
}

.activity-points {
  color: var(--primary-color);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.info-item:last-child {
  border-bottom: none;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group span {
  color: var(--text-primary);
  font-weight: 700;
}

.full-width {
  grid-column: 1 / -1;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-base);
  color: var(--text-primary);
  font: inherit;
}

.form-textarea {
  resize: vertical;
}

@media (max-width: 980px) {
  .hero-card,
  .overview-grid {
    grid-template-columns: 1fr;
  }

  .hero-card {
    flex-direction: column;
  }
}

@media (max-width: 760px) {
  .hero-stats,
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
