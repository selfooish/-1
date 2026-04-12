<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useGrowthStore } from '@/stores/growth'
import { useUserStore } from '@/stores/user'
import { getLevelFromPoints } from '@/utils'

const growthStore = useGrowthStore()
const userStore = useUserStore()

const user = computed(() => userStore.userInfo)
const totalPoints = computed(() => user.value?.points || growthStore.totalPoints)
const levelInfo = computed(() => getLevelFromPoints(totalPoints.value))
const pointRecords = computed(() => growthStore.pointRecords)
const badges = computed(() => growthStore.badges)
const unlockedBadges = computed(() => growthStore.unlockedBadges)
const growthData = computed(() => growthStore.growthData)
const maxDailyPoints = computed(() => Math.max(...growthData.value.map((item) => item.points), 1))

async function loadGrowthData() {
  await Promise.all([
    userStore.fetchUserInfo(),
    growthStore.fetchPointRecords(),
    growthStore.fetchBadges(),
    growthStore.fetchGrowthData(30),
  ])
}

onMounted(loadGrowthData)
</script>

<template>
  <div class="growth-shell">
    <div class="hero-card">
      <div class="hero-main">
        <p class="eyebrow">Growth Center</p>
        <h1>成长中心</h1>
        <p>这一页现在直接使用积分记录、徽章列表和成长曲线接口。</p>
      </div>
      <div class="hero-side">
        <div class="level-badge">Lv.{{ levelInfo.level }}</div>
        <div class="level-title">{{ levelInfo.title }}</div>
        <div class="level-points">{{ totalPoints }} 积分</div>
      </div>
    </div>

    <section class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ pointRecords.length }}</div>
        <div class="stat-label">积分记录</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ unlockedBadges.length }}</div>
        <div class="stat-label">已解锁徽章</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ badges.length - unlockedBadges.length }}</div>
        <div class="stat-label">待完成徽章</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ growthData.length }}</div>
        <div class="stat-label">成长天数</div>
      </div>
    </section>

    <div class="content-grid">
      <section class="panel-card">
        <div class="panel-header">
          <h2>我的徽章</h2>
          <span>{{ unlockedBadges.length }}/{{ badges.length }}</span>
        </div>
        <div class="badge-grid">
          <div
            v-for="badge in badges"
            :key="badge.id"
            class="badge-card"
            :class="{ locked: !badge.unlockedAt }"
            :style="{ borderColor: badge.color }"
          >
            <div class="badge-icon">{{ badge.unlockedAt ? badge.icon : '未解锁' }}</div>
            <div class="badge-name">{{ badge.name }}</div>
            <div class="badge-desc">{{ badge.description }}</div>
            <div class="badge-meta">
              <span v-if="badge.unlockedAt">已获得</span>
              <span v-else>{{ badge.progress || 0 }}/{{ badge.total || 0 }}</span>
            </div>
          </div>
        </div>
      </section>

      <section class="panel-card">
        <div class="panel-header">
          <h2>积分记录</h2>
          <span>最近 {{ pointRecords.length }} 条</span>
        </div>
        <div class="record-list">
          <div v-for="record in pointRecords" :key="record.id" class="record-item">
            <div>
              <div class="record-action">{{ record.action }}</div>
              <div class="record-date">{{ record.createdAt.slice(0, 10) }}</div>
            </div>
            <strong class="record-points">+{{ record.points }}</strong>
          </div>
        </div>
      </section>
    </div>

    <section class="panel-card">
      <div class="panel-header">
        <h2>30 天成长曲线</h2>
        <span>来自 /growth</span>
      </div>
      <div class="chart-wrap">
        <div
          v-for="item in growthData"
          :key="item.date"
          class="bar-group"
          :title="`${item.date}: ${item.points} 积分`"
        >
          <div
            class="bar"
            :style="{ height: `${(item.points / maxDailyPoints) * 100}%` }"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.growth-shell {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero-card {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 28px 32px;
  border-radius: var(--radius-xl);
  background: linear-gradient(135deg, #174c39, #2c7b5d);
  color: #fff;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.8;
}

.hero-main h1 {
  margin: 0 0 10px;
  font-size: 34px;
}

.hero-main p:last-child {
  margin: 0;
  line-height: 1.7;
}

.hero-side {
  min-width: 180px;
  text-align: right;
}

.level-badge {
  font-size: 36px;
  font-weight: 800;
}

.level-title {
  margin-top: 8px;
  font-weight: 700;
}

.level-points {
  margin-top: 6px;
  opacity: 0.85;
}

.stats-grid,
.content-grid,
.badge-grid {
  display: grid;
  gap: 16px;
}

.stats-grid {
  grid-template-columns: repeat(4, 1fr);
}

.content-grid {
  grid-template-columns: 1.2fr 1fr;
}

.badge-grid {
  grid-template-columns: repeat(3, 1fr);
}

.stat-card,
.panel-card,
.badge-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.stat-card {
  padding: 18px;
}

.stat-value {
  font-size: 28px;
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
  color: var(--text-primary);
  font-size: 22px;
}

.panel-header span {
  color: var(--text-muted);
}

.badge-card {
  padding: 16px;
}

.badge-card.locked {
  opacity: 0.6;
}

.badge-icon {
  font-weight: 700;
  color: var(--text-primary);
}

.badge-name {
  margin-top: 12px;
  font-weight: 700;
  color: var(--text-primary);
}

.badge-desc {
  margin-top: 8px;
  color: var(--text-muted);
  line-height: 1.6;
  font-size: 14px;
}

.badge-meta {
  margin-top: 12px;
  color: var(--primary-color);
  font-weight: 700;
  font-size: 14px;
}

.record-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  background: var(--bg-base);
  border: 1px solid var(--border-color);
}

.record-action {
  color: var(--text-primary);
  font-weight: 700;
}

.record-date {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 14px;
}

.record-points {
  color: var(--primary-color);
}

.chart-wrap {
  display: flex;
  align-items: end;
  gap: 6px;
  height: 180px;
}

.bar-group {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: end;
}

.bar {
  width: 100%;
  min-height: 4px;
  border-radius: 8px 8px 0 0;
  background: linear-gradient(180deg, #7ed7b0, #2c7b5d);
}

@media (max-width: 1100px) {
  .stats-grid,
  .badge-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .hero-card,
  .stats-grid,
  .badge-grid {
    grid-template-columns: 1fr;
  }

  .hero-card {
    flex-direction: column;
  }

  .hero-side {
    text-align: left;
  }
}
</style>
