<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG } from '@/utils'

const taskList = ref([
  { id: 1, title: '完成一次电饭煲清洁与维护', description: '将家中电饭煲拆解清洗，并记录清洁前后对比照片', category: '家电维修', coverImage: 'https://picsum.photos/seed/task1/400/200', points: 50, difficulty: 'easy' as const, deadline: '2025-02-28', status: 'pending' as const, submitCount: 0, maxSubmits: 1 },
  { id: 2, title: '整理衣柜：按季节分类收纳', description: '对衣柜进行彻底整理，按季节和类型分类，拍照记录整理效果', category: '收纳整理', coverImage: 'https://picsum.photos/seed/task2/400/200', points: 40, difficulty: 'easy' as const, deadline: '2025-03-15', status: 'pending' as const, submitCount: 0, maxSubmits: 1 },
  { id: 3, title: '养护一株绿萝并记录成长', description: '选择一株绿萝进行养护，每周记录一次生长状态，共记录4周', category: '绿植养护', coverImage: 'https://picsum.photos/seed/task3/400/200', points: 80, difficulty: 'medium' as const, deadline: '2025-04-01', status: 'pending' as const, submitCount: 0, maxSubmits: 1 },
  { id: 4, title: '手工制作：布艺收纳袋', description: '利用旧衣物或布料，亲手缝制一个实用收纳袋', category: '手工制作', coverImage: 'https://picsum.photos/seed/task4/400/200', points: 60, difficulty: 'easy' as const, deadline: '2025-03-20', status: 'pending' as const, submitCount: 0, maxSubmits: 1 },
  { id: 5, title: '家庭安全自查：排查用电隐患', description: '对家中用电安全进行自查，识别并记录至少3处安全隐患，提出改进建议', category: '安全常识', coverImage: 'https://picsum.photos/seed/task5/400/200', points: 70, difficulty: 'medium' as const, deadline: '2025-03-10', status: 'pending' as const, submitCount: 0, maxSubmits: 1 },
  { id: 6, title: '厨房大扫除清洁记录', description: '对厨房进行一次深度清洁，拍照记录清洁过程和成果', category: '清洁卫生', coverImage: 'https://picsum.photos/seed/task6/400/200', points: 45, difficulty: 'easy' as const, deadline: '2025-02-20', status: 'pending' as const, submitCount: 0, maxSubmits: 1 },
])
</script>

<template>
  <div class="task-list-view">
    <div class="page-header">
      <h1 class="page-title"><span>🎯</span> 实践任务</h1>
      <p class="page-desc">在生活中实践所学技能，上传成果照片或视频，获得积分奖励！</p>
    </div>

    <div class="task-grid">
      <RouterLink
        v-for="task in taskList"
        :key="task.id"
        :to="`/tasks/${task.id}`"
        class="task-card"
      >
        <div class="task-cover">
          <img :src="task.coverImage" :alt="task.title" />
          <div class="task-points">+{{ task.points }} 积分</div>
          <div class="task-difficulty"
            :style="{ background: DIFFICULTY_CONFIG[task.difficulty]?.bgColor, color: DIFFICULTY_CONFIG[task.difficulty]?.color }">
            {{ DIFFICULTY_CONFIG[task.difficulty]?.label }}
          </div>
          <div class="task-category"
            :style="{ background: CATEGORY_CONFIG[task.category]?.color }">
            {{ CATEGORY_CONFIG[task.category]?.icon }} {{ task.category }}
          </div>
        </div>
        <div class="task-info">
          <h3 class="task-title">{{ task.title }}</h3>
          <p class="task-desc">{{ task.description }}</p>
          <div class="task-footer">
            <span class="task-deadline">📅 {{ task.deadline }}</span>
            <button class="task-btn" @click.prevent="() => {}">
              领取任务 →
            </button>
          </div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.page-header { margin-bottom: 32px; }
.page-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.page-desc { font-size: 0.9rem; color: var(--text-muted); }
.task-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.task-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}
.task-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
.task-cover {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
}
.task-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}
.task-card:hover .task-cover img { transform: scale(1.05); }
.task-points {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(66, 184, 131, 0.9);
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 700;
}
.task-difficulty {
  position: absolute;
  bottom: 10px;
  right: 10px;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
}
.task-category {
  position: absolute;
  bottom: 10px;
  left: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.68rem;
  color: #fff;
  font-weight: 600;
}
.task-info { padding: 16px; flex: 1; display: flex; flex-direction: column; gap: 8px; }
.task-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.task-desc {
  font-size: 0.8rem;
  color: var(--text-muted);
  line-height: 1.5;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
}
.task-deadline { font-size: 0.75rem; color: var(--text-muted); }
.task-btn {
  padding: 5px 12px;
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.task-btn:hover { background: var(--primary-color-dark); }
@media (max-width: 1024px) { .task-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .task-grid { grid-template-columns: 1fr; } }
</style>
