<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { ElInput, ElOption, ElSelect } from 'element-plus'
import { useTutorialStore } from '@/stores/tutorial'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG, getAvatarBg } from '@/utils'
import type { TutorialCategory } from '@/types'

const route = useRoute()
const router = useRouter()
const tutorialStore = useTutorialStore()

const selectedCategory = ref<TutorialCategory | ''>((route.query.category as string) || '')
const selectedDifficulty = ref((route.query.difficulty as string) || '')
const keyword = ref((route.query.keyword as string) || '')

const tutorials = computed(() => tutorialStore.tutorials)
const loading = computed(() => tutorialStore.loading)

async function loadTutorials() {
  await tutorialStore.fetchTutorials({
    category: selectedCategory.value,
    difficulty: selectedDifficulty.value,
    keyword: keyword.value.trim(),
    page: 1,
    pageSize: 20,
  })
}

function syncQuery() {
  router.replace({
    query: {
      category: selectedCategory.value || undefined,
      difficulty: selectedDifficulty.value || undefined,
      keyword: keyword.value || undefined,
    },
  })
}

function resetFilters() {
  selectedCategory.value = ''
  selectedDifficulty.value = ''
  keyword.value = ''
}

watch([selectedCategory, selectedDifficulty, keyword], async () => {
  syncQuery()
  await loadTutorials()
})

onMounted(loadTutorials)
</script>

<template>
  <div class="page-shell">
    <div class="page-header">
      <div>
        <p class="eyebrow">Tutorials</p>
        <h1 class="page-title">技能教程</h1>
        <p class="page-desc">现在列表数据来自 FastAPI，筛选会直接请求后端接口。</p>
      </div>
    </div>

    <div class="filter-bar">
      <el-input v-model="keyword" placeholder="搜索教程标题" clearable class="filter-input" />
      <el-select v-model="selectedCategory" placeholder="全部分类" clearable class="filter-select">
        <el-option
          v-for="(cfg, key) in CATEGORY_CONFIG"
          :key="key"
          :label="cfg.label"
          :value="key"
        />
      </el-select>
      <el-select v-model="selectedDifficulty" placeholder="全部难度" clearable class="filter-select">
        <el-option label="入门" value="easy" />
        <el-option label="进阶" value="medium" />
        <el-option label="高级" value="hard" />
      </el-select>
      <button class="btn btn-outline" @click="resetFilters">重置</button>
      <span class="filter-count">共 {{ tutorialStore.total }} 条</span>
    </div>

    <div v-if="loading" class="state-card">正在加载教程...</div>

    <div v-else-if="tutorials.length" class="card-grid">
      <RouterLink
        v-for="tutorial in tutorials"
        :key="tutorial.id"
        :to="`/tutorials/${tutorial.id}`"
        class="content-card"
      >
        <img :src="tutorial.coverImage" :alt="tutorial.title" class="card-cover" />
        <div class="card-body">
          <div class="meta-row">
            <span
              class="pill"
              :style="{ background: CATEGORY_CONFIG[tutorial.category]?.color || '#64748b' }"
            >
              {{ CATEGORY_CONFIG[tutorial.category]?.label || tutorial.category }}
            </span>
            <span
              class="pill pill-light"
              :style="{
                color: DIFFICULTY_CONFIG[tutorial.difficulty]?.color,
                background: DIFFICULTY_CONFIG[tutorial.difficulty]?.bgColor,
              }"
            >
              {{ DIFFICULTY_CONFIG[tutorial.difficulty]?.label }}
            </span>
          </div>

          <h3 class="card-title">{{ tutorial.title }}</h3>
          <p class="card-desc">{{ tutorial.description }}</p>

          <div class="author-row">
            <span class="avatar" :style="{ background: getAvatarBg(tutorial.author) }">
              {{ tutorial.author?.[0] || 'A' }}
            </span>
            <span>{{ tutorial.author }}</span>
            <span class="muted">浏览 {{ tutorial.viewCount }}</span>
          </div>
        </div>
      </RouterLink>
    </div>

    <div v-else class="state-card">没有查到符合条件的教程。</div>
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
  align-items: center;
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
  font-size: 32px;
  font-weight: 800;
  color: var(--text-primary);
}

.page-desc {
  margin: 8px 0 0;
  color: var(--text-muted);
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  padding: 18px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.filter-input {
  max-width: 260px;
}

.filter-select {
  width: 180px;
}

.filter-count {
  margin-left: auto;
  color: var(--text-muted);
  font-size: 14px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}

.content-card {
  overflow: hidden;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.content-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-cover {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

.card-body {
  padding: 16px;
}

.meta-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
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

.card-title {
  margin: 0 0 8px;
  color: var(--text-primary);
  font-size: 18px;
  line-height: 1.4;
}

.card-desc {
  margin: 0 0 14px;
  color: var(--text-muted);
  line-height: 1.6;
}

.author-row {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
}

.avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}

.muted {
  margin-left: auto;
  color: var(--text-muted);
}

.state-card {
  padding: 48px 20px;
  border-radius: var(--radius-lg);
  border: 1px dashed var(--border-color);
  background: var(--bg-card);
  text-align: center;
  color: var(--text-muted);
}
</style>
