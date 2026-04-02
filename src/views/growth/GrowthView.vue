<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useGrowthStore } from '@/stores/growth'
import { getLevelFromPoints } from '@/utils'

const userStore = useUserStore()
const growthStore = useGrowthStore()

const totalPoints = ref(850)
const levelInfo = computed(() => getLevelFromPoints(totalPoints.value))

const badges = ref([
  { id: 1, name: '初学者', description: '完成第一个教程', icon: '🌱', color: '#42b883', type: 'skill' as const, unlockedAt: '2025-01-10', progress: 1, total: 1 },
  { id: 2, name: '答题达人', description: '完成10次答题', icon: '📝', color: '#3498db', type: 'quiz' as const, unlockedAt: '2025-01-15', progress: 10, total: 10 },
  { id: 3, name: '任务达人', description: '完成5个实践任务', icon: '🎯', color: '#e67e22', type: 'task' as const, unlockedAt: '2025-01-20', progress: 5, total: 5 },
  { id: 4, name: '全能选手', description: '完成所有分类的教程', icon: '🏆', color: '#9b59b6', type: 'special' as const, unlockedAt: undefined, progress: 6, total: 8 },
  { id: 5, name: '连续7天学习', description: '每日签到7天', icon: '🔥', color: '#e74c3c', type: 'streak' as const, unlockedAt: undefined, progress: 3, total: 7 },
  { id: 6, name: '满分答题', description: '某次答题获得满分', icon: '💯', color: '#f39c12', type: 'quiz' as const, unlockedAt: '2025-01-18', progress: 1, total: 1 },
])

const pointRecords = ref([
  { id: 1, type: 'tutorial', action: '完成教程《电饭煲维修》', points: 30, createdAt: '2025-01-20' },
  { id: 2, type: 'quiz', action: '家电维修测验获得85分', points: 50, createdAt: '2025-01-19' },
  { id: 3, type: 'task', action: '任务「电饭煲清洁」获优秀', points: 80, createdAt: '2025-01-18' },
  { id: 4, type: 'daily', action: '每日签到奖励', points: 10, createdAt: '2025-01-17' },
  { id: 5, type: 'review', action: '审核他人任务成果', points: 15, createdAt: '2025-01-16' },
  { id: 6, type: 'tutorial', action: '完成教程《绿萝养护》', points: 25, createdAt: '2025-01-15' },
])

// 模拟成长数据
const growthDays = ref(Array.from({ length: 30 }, (_, i) => {
  const d = new Date()
  d.setDate(d.getDate() - (29 - i))
  return {
    date: d.toISOString().split('T')[0],
    points: Math.floor(Math.random() * 80),
    tasksCompleted: Math.floor(Math.random() * 2),
    tutorialsCompleted: Math.floor(Math.random() * 1),
    quizzesTaken: Math.floor(Math.random() * 1),
  }
}))

const maxDailyPoints = computed(() => Math.max(...growthDays.value.map(d => d.points), 1))

onMounted(() => {
  if (userStore.isLoggedIn) {
    userStore.fetchUserInfo()
    growthStore.fetchGrowthData()
  }
})
</script>

<template>
  <div class="growth-view">
    <div class="page-header">
      <h1 class="page-title"><span>🌱</span> 成长中心</h1>
      <p class="page-desc">记录你的每一步成长，见证从新手到达人的蜕变</p>
    </div>

    <!-- 等级卡 -->
    <div class="level-card">
      <div class="level-info">
        <div class="level-badge">
          <span class="level-num">{{ levelInfo.level }}</span>
        </div>
        <div>
          <div class="level-title">{{ levelInfo.title }}</div>
          <div class="level-desc">
            <span class="points-display">⭐ {{ totalPoints }} 积分</span>
            <span class="level-next">再获得 {{ 100 - totalPoints % 100 }} 积分升级</span>
          </div>
        </div>
      </div>
      <div class="level-progress">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: levelInfo.progress + '%' }" />
        </div>
        <div class="level-markers">
          <span>Lv.{{ levelInfo.level }}</span>
          <span>Lv.{{ levelInfo.level + 1 }}</span>
        </div>
      </div>
    </div>

    <!-- 勋章展示 -->
    <section class="section">
      <h2 class="section-title"><span>🏅</span> 我的勋章</h2>
      <div class="badges-grid">
        <div
          v-for="badge in badges"
          :key="badge.id"
          class="badge-card"
          :class="{ unlocked: badge.unlockedAt }"
          :style="{ '--badge-color': badge.color }"
        >
          <div class="badge-icon">{{ badge.unlockedAt ? badge.icon : '🔒' }}</div>
          <div class="badge-name">{{ badge.name }}</div>
          <div class="badge-desc">{{ badge.description }}</div>
          <div v-if="!badge.unlockedAt" class="badge-progress">
            <div class="badge-progress-bar">
              <div class="badge-progress-fill" :style="{ width: (badge.progress / badge.total * 100) + '%' }" />
            </div>
            <span>{{ badge.progress }}/{{ badge.total }}</span>
          </div>
          <div v-else class="badge-date">{{ badge.unlockedAt }} 获得</div>
        </div>
      </div>
    </section>

    <!-- 积分记录 -->
    <section class="section">
      <h2 class="section-title"><span>📜</span> 积分记录</h2>
      <div class="records-list">
        <div v-for="record in pointRecords" :key="record.id" class="record-item">
          <div class="record-icon" :class="record.type">
            {{ record.type === 'tutorial' ? '🎬' : record.type === 'quiz' ? '📝' : record.type === 'task' ? '🎯' : record.type === 'daily' ? '📅' : '✅' }}
          </div>
          <div class="record-info">
            <div class="record-action">{{ record.action }}</div>
            <div class="record-date">{{ record.createdAt }}</div>
          </div>
          <div class="record-points">+{{ record.points }}</div>
        </div>
      </div>
    </section>

    <!-- 成长曲线 -->
    <section class="section">
      <h2 class="section-title"><span>📈</span> 30天成长曲线</h2>
      <div class="chart-card">
        <div class="chart-bars">
          <div
            v-for="day in growthDays"
            :key="day.date"
            class="chart-bar-wrap"
            :title="`${day.date}: ${day.points} 积分`"
          >
            <div
              class="chart-bar"
              :style="{ height: (day.points / maxDailyPoints * 100) + '%' }"
            />
          </div>
        </div>
        <div class="chart-legend">
          <span>最近 30 天</span>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.growth-view {}

.page-header { margin-bottom: 32px; }
.page-title { font-size: 1.8rem; font-weight: 800; color: var(--text-primary); margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
.page-desc { font-size: 0.9rem; color: var(--text-muted); }

.level-card {
  background: linear-gradient(135deg, #1a4a2e, #2d7a4e);
  border-radius: var(--radius-xl);
  padding: 28px 32px;
  margin-bottom: 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.level-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.level-badge {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(255,255,255,0.15);
  border: 3px solid rgba(255,255,255,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.level-num {
  font-size: 2rem;
  font-weight: 900;
  color: #fff;
}

.level-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 6px;
}

.level-desc {
  display: flex;
  gap: 16px;
  font-size: 0.85rem;
  color: rgba(255,255,255,0.8);
}

.points-display {
  color: #ffd700;
  font-weight: 700;
}

.level-progress {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.progress-bar {
  height: 8px;
  background: rgba(255,255,255,0.15);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ffd700, #ffec8b);
  border-radius: 4px;
  transition: width 0.5s;
}

.level-markers {
  display: flex;
  justify-content: space-between;
  font-size: 0.72rem;
  color: rgba(255,255,255,0.5);
}

.section { margin-bottom: 40px; }
.section-title { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }

.badges-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 14px;
}

.badge-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 16px 12px;
  text-align: center;
  transition: all 0.3s;
  opacity: 0.5;
}

.badge-card.unlocked {
  opacity: 1;
  border-color: var(--badge-color);
  background: rgba(var(--badge-color), 0.03);
}

.badge-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.badge-icon {
  font-size: 2.2rem;
  margin-bottom: 8px;
}

.badge-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.badge-desc {
  font-size: 0.7rem;
  color: var(--text-muted);
  line-height: 1.4;
  margin-bottom: 8px;
}

.badge-progress {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.7rem;
  color: var(--text-muted);
}

.badge-progress-bar {
  flex: 1;
  height: 4px;
  background: var(--bg-soft);
  border-radius: 2px;
  overflow: hidden;
}

.badge-progress-fill {
  height: 100%;
  background: var(--badge-color);
  border-radius: 2px;
}

.badge-date {
  font-size: 0.68rem;
  color: var(--badge-color);
  font-weight: 600;
}

.records-list {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.record-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border-color);
  transition: background 0.2s;
}

.record-item:last-child {
  border-bottom: none;
}

.record-item:hover {
  background: var(--bg-soft);
}

.record-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.record-info {
  flex: 1;
}

.record-action {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.record-date {
  font-size: 0.72rem;
  color: var(--text-muted);
}

.record-points {
  font-size: 1rem;
  font-weight: 800;
  color: var(--primary-color);
}

.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 3px;
  height: 120px;
}

.chart-bar-wrap {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: flex-end;
  cursor: pointer;
}

.chart-bar {
  width: 100%;
  background: linear-gradient(to top, var(--primary-color), var(--primary-color-light));
  border-radius: 2px 2px 0 0;
  transition: height 0.3s;
  min-height: 2px;
  opacity: 0.7;
}

.chart-bar-wrap:hover .chart-bar {
  opacity: 1;
}

.chart-legend {
  text-align: center;
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 8px;
}

@media (max-width: 1024px) { .badges-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .badges-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
