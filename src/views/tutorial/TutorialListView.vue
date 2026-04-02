<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useTutorialStore } from '@/stores/tutorial'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG, getAvatarBg } from '@/utils'
import { ElSelect, ElOption, ElInput } from 'element-plus'
import type { TutorialCategory } from '@/types'

const route = useRoute()
const router = useRouter()
const tutorialStore = useTutorialStore()

const selectedCategory = ref<TutorialCategory | ''>((route.query.category as any) || '')
const selectedDifficulty = ref('')
const keyword = ref((route.query.keyword as string) || '')
const currentPage = ref(1)
const pageSize = ref(20)

// 模拟数据
const tutorials = ref([
  {
    id: 1, title: '电饭煲常见故障与维修', category: '家电维修' as TutorialCategory,
    coverImage: 'https://picsum.photos/seed/elec/400/250', description: '从拆解到维修，详细讲解电饭煲不通电、加热异常等常见问题',
    duration: '2h30m', difficulty: 'medium' as const, author: '王师傅', viewCount: 2341, rating: 4.8, reviewCount: 156,
  },
  {
    id: 2, title: '衣柜收纳全攻略', category: '收纳整理' as TutorialCategory,
    coverImage: 'https://picsum.photos/seed/closet/400/250', description: '科学的分类方法，让衣柜整洁有序，每天出门不再慌张',
    duration: '1h15m', difficulty: 'easy' as const, author: '小莉', viewCount: 4102, rating: 4.9, reviewCount: 289,
  },
  {
    id: 3, title: '绿萝养护与繁殖技巧', category: '绿植养护' as TutorialCategory,
    coverImage: 'https://picsum.photos/seed/plant/400/250', description: '零基础学会绿萝养护，从浇水施肥到扦插繁殖全教程',
    duration: '45m', difficulty: 'easy' as const, author: '园艺师阿明', viewCount: 1876, rating: 4.7, reviewCount: 98,
  },
  {
    id: 4, title: '家庭手工：布艺收纳袋', category: '手工制作' as TutorialCategory,
    coverImage: 'https://picsum.photos/seed/craft/400/250', description: '旧衣物变废为宝，亲手缝制实用布艺收纳袋',
    duration: '1h', difficulty: 'easy' as const, author: '手工达人小美', viewCount: 3201, rating: 4.6, reviewCount: 201,
  },
  {
    id: 5, title: '家庭用电安全与故障排查', category: '安全常识' as TutorialCategory,
    coverImage: 'https://picsum.photos/seed/safety/400/250', description: '掌握家庭用电安全知识，学会简单电路故障排查',
    duration: '1h40m', difficulty: 'medium' as const, author: '电力工程师老张', viewCount: 5621, rating: 4.8, reviewCount: 334,
  },
  {
    id: 6, title: '熨斗使用与衣物保养', category: '衣物护理' as TutorialCategory,
    coverImage: 'https://picsum.photos/seed/iron/400/250', description: '不同材质衣物的熨烫技巧，让衣物焕然一新',
    duration: '55m', difficulty: 'easy' as const, author: '形象顾问Lisa', viewCount: 1890, rating: 4.5, reviewCount: 112,
  },
  {
    id: 7, title: '厨房深度清洁指南', category: '清洁卫生' as TutorialCategory,
    coverImage: 'https://picsum.photos/seed/clean/400/250', description: '厨房各区域的清洁技巧，去除油污与细菌',
    duration: '1h20m', difficulty: 'easy' as const, author: '保洁达人阿花', viewCount: 2903, rating: 4.7, reviewCount: 187,
  },
  {
    id: 8, title: '微波炉常见问题DIY维修', category: '家电维修' as TutorialCategory,
    coverImage: 'https://picsum.photos/seed/microwave/400/250', description: '微波炉不通电、不加热等问题自检与维修',
    duration: '1h50m', difficulty: 'hard' as const, author: '王师傅', viewCount: 1542, rating: 4.4, reviewCount: 89,
  },
])

const filteredTutorials = computed(() => {
  return tutorials.value.filter(t => {
    if (selectedCategory.value && t.category !== selectedCategory.value) return false
    if (selectedDifficulty.value && t.difficulty !== selectedDifficulty.value) return false
    if (keyword.value && !t.title.includes(keyword.value)) return false
    return true
  })
})

function resetFilters() {
  selectedCategory.value = ''
  selectedDifficulty.value = ''
  keyword.value = ''
  currentPage.value = 1
}

onMounted(() => {})
</script>

<template>
  <div class="tutorial-list-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <span>🎬</span> 技能教程
      </h1>
      <p class="page-desc">涵盖家电维修、收纳整理、绿植养护、手工制作、安全常识等分类的精品视频教程</p>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-input
        v-model="keyword"
        placeholder="搜索教程..."
        style="width:220px"
        clearable
      >
        <template #prefix>🔍</template>
      </el-input>
      <el-select v-model="selectedCategory" placeholder="全部分类" style="width:160px" clearable>
        <el-option
          v-for="(cfg, key) in CATEGORY_CONFIG"
          :key="key"
          :label="cfg.label"
          :value="key"
        />
      </el-select>
      <el-select v-model="selectedDifficulty" placeholder="难度" style="width:120px" clearable>
        <el-option label="入门" value="easy" />
        <el-option label="进阶" value="medium" />
        <el-option label="高级" value="hard" />
      </el-select>
      <button class="btn btn-outline btn-sm" @click="resetFilters">重置</button>
      <span class="filter-count">共 {{ filteredTutorials.length }} 个教程</span>
    </div>

    <!-- 分类快捷入口 -->
    <div class="category-tabs">
      <button
        class="cat-tab"
        :class="{ active: selectedCategory === '' }"
        @click="selectedCategory = ''"
      >全部</button>
      <button
        v-for="(cfg, key) in CATEGORY_CONFIG"
        :key="key"
        class="cat-tab"
        :class="{ active: selectedCategory === key }"
        :style="selectedCategory === key ? { borderColor: cfg.color, color: cfg.color } : {}"
        @click="selectedCategory = key as TutorialCategory"
      >
        {{ cfg.icon }} {{ cfg.label }}
      </button>
    </div>

    <!-- 教程列表 -->
    <div v-if="filteredTutorials.length > 0" class="tutorials-grid">
      <RouterLink
        v-for="t in filteredTutorials"
        :key="t.id"
        :to="`/tutorials/${t.id}`"
        class="tutorial-card"
      >
        <div class="tutorial-cover">
          <img :src="t.coverImage" :alt="t.title" />
          <div class="tutorial-overlay"><span class="play-btn">▶</span></div>
          <div class="tutorial-difficulty"
            :style="{ background: DIFFICULTY_CONFIG[t.difficulty]?.bgColor, color: DIFFICULTY_CONFIG[t.difficulty]?.color }">
            {{ DIFFICULTY_CONFIG[t.difficulty]?.label }}
          </div>
          <div class="tutorial-duration">⏱ {{ t.duration }}</div>
          <div class="tutorial-category-tag"
            :style="{ background: CATEGORY_CONFIG[t.category]?.color }">
            {{ CATEGORY_CONFIG[t.category]?.icon }} {{ t.category }}
          </div>
        </div>
        <div class="tutorial-info">
          <h3 class="tutorial-title">{{ t.title }}</h3>
          <p class="tutorial-desc">{{ t.description }}</p>
          <div class="tutorial-meta">
            <span class="tutorial-author">
              <span class="author-avatar" :style="{ background: getAvatarBg(t.author) }">{{ t.author[0] }}</span>
              {{ t.author }}
            </span>
            <span>👁 {{ t.viewCount }}</span>
            <span>⭐ {{ t.rating }}</span>
          </div>
        </div>
      </RouterLink>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">🔍</div>
      <p>没有找到符合条件的教程</p>
      <button class="btn btn-primary" @click="resetFilters">清除筛选</button>
    </div>
  </div>
</template>

<style scoped>
.tutorial-list-view {}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-desc {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}

.filter-count {
  margin-left: auto;
  font-size: 0.82rem;
  color: var(--text-muted);
}

.category-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

.cat-tab {
  padding: 6px 14px;
  border: 1.5px solid var(--border-color);
  border-radius: 20px;
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s;
}

.cat-tab:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.cat-tab.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: #fff;
}

.tutorials-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.tutorial-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.tutorial-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.tutorial-cover {
  position: relative;
  aspect-ratio: 16/10;
  overflow: hidden;
}

.tutorial-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.tutorial-card:hover .tutorial-cover img {
  transform: scale(1.05);
}

.tutorial-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.tutorial-card:hover .tutorial-overlay {
  opacity: 1;
}

.play-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255,255,255,0.9);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  padding-left: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.tutorial-difficulty {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
}

.tutorial-duration {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0,0,0,0.6);
  color: #fff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.72rem;
}

.tutorial-category-tag {
  position: absolute;
  bottom: 10px;
  left: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.68rem;
  color: #fff;
  font-weight: 600;
}

.tutorial-info {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tutorial-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tutorial-desc {
  font-size: 0.8rem;
  color: var(--text-muted);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.tutorial-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 0.78rem;
  color: var(--text-muted);
  gap: 8px;
}

.tutorial-author {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-shrink: 0;
}

.author-avatar {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6rem;
  color: #fff;
  font-weight: 700;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-state p {
  margin-bottom: 16px;
}

@media (max-width: 1024px) {
  .tutorials-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .tutorials-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .tutorials-grid {
    grid-template-columns: 1fr;
  }
}
</style>
