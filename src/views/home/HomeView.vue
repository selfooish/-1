<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useTutorialStore } from '@/stores/tutorial'
import { useUserStore } from '@/stores/user'
import { CATEGORY_CONFIG, DIFFICULTY_CONFIG, getAvatarBg } from '@/utils'

const router = useRouter()
const tutorialStore = useTutorialStore()
const userStore = useUserStore()

const featuredTutorials = ref([
  {
    id: 1,
    title: '电饭煲常见故障与维修',
    category: '家电维修',
    coverImage: 'https://picsum.photos/seed/elec/400/250',
    description: '从拆解到维修，详细讲解电饭煲不通电、加热异常等常见问题',
    duration: '2h30m',
    difficulty: 'medium',
    author: '王师傅',
    viewCount: 2341,
    rating: 4.8,
    reviewCount: 156,
  },
  {
    id: 2,
    title: '衣柜收纳全攻略',
    category: '收纳整理',
    coverImage: 'https://picsum.photos/seed/closet/400/250',
    description: '科学的分类方法，让衣柜整洁有序，每天出门不再慌张',
    duration: '1h15m',
    difficulty: 'easy',
    author: '小莉',
    viewCount: 4102,
    rating: 4.9,
    reviewCount: 289,
  },
  {
    id: 3,
    title: '绿萝养护与繁殖技巧',
    category: '绿植养护',
    coverImage: 'https://picsum.photos/seed/plant/400/250',
    description: '零基础学会绿萝养护，从浇水施肥到扦插繁殖全教程',
    duration: '45m',
    difficulty: 'easy',
    author: '园艺师阿明',
    viewCount: 1876,
    rating: 4.7,
    reviewCount: 98,
  },
  {
    id: 4,
    title: '家庭手工：布艺收纳袋',
    category: '手工制作',
    coverImage: 'https://picsum.photos/seed/craft/400/250',
    description: '旧衣物变废为宝，亲手缝制实用布艺收纳袋',
    duration: '1h',
    difficulty: 'easy',
    author: '手工达人小美',
    viewCount: 3201,
    rating: 4.6,
    reviewCount: 201,
  },
])

const stats = ref([
  { icon: '📚', value: '280+', label: '精品教程' },
  { icon: '📝', value: '5000+', label: '题库题目' },
  { icon: '🎯', value: '1.2万', label: '学习人次' },
  { icon: '🏆', value: '98%', label: '好评率' },
])

const categories = Object.values(CATEGORY_CONFIG)
const bannerSlide = ref(0)

function nextBanner() {
  bannerSlide.value = (bannerSlide.value + 1) % 3
}

onMounted(() => {
  setInterval(nextBanner, 5000)
  if (userStore.isLoggedIn) {
    userStore.fetchUserInfo()
  }
})
</script>

<template>
  <div class="home-view">
    <!-- Banner -->
    <section class="hero-banner">
      <div class="banner-slides" :style="{ transform: `translateX(-${bannerSlide * 100}%)` }">
        <div class="banner-slide slide-1">
          <div class="banner-content">
            <div class="banner-tag">🔥 热门推荐</div>
            <h1 class="banner-title">掌握劳动技能<br>点亮成长之路</h1>
            <p class="banner-desc">家电维修 · 收纳整理 · 绿植养护 · 手工制作 · 安全常识</p>
            <div class="banner-actions">
              <RouterLink to="/tutorials" class="btn btn-primary btn-lg">开始学习</RouterLink>
              <RouterLink to="/tasks" class="btn btn-outline btn-lg" style="border-color:rgba(255,255,255,0.4);color:#fff;">参与实践</RouterLink>
            </div>
          </div>
        </div>
        <div class="banner-slide slide-2">
          <div class="banner-content">
            <div class="banner-tag">🎯 在线答题</div>
            <h1 class="banner-title">趣味答题挑战<br>检验学习成果</h1>
            <p class="banner-desc">涵盖所有劳动技能分类的题库，随时检验学习成果</p>
            <div class="banner-actions">
              <RouterLink to="/quizzes" class="btn btn-primary btn-lg">去答题</RouterLink>
            </div>
          </div>
        </div>
        <div class="banner-slide slide-3">
          <div class="banner-content">
            <div class="banner-tag">🌟 勋章成就</div>
            <h1 class="banner-title">积分勋章激励<br>见证每一步成长</h1>
            <p class="banner-desc">完成教程、答题、任务，获得积分与专属勋章</p>
            <div class="banner-actions">
              <RouterLink to="/growth" class="btn btn-primary btn-lg">查看成长</RouterLink>
            </div>
          </div>
        </div>
      </div>
      <div class="banner-dots">
        <button v-for="i in 3" :key="i" class="dot" :class="{ active: bannerSlide === i - 1 }" @click="bannerSlide = i - 1" />
      </div>
    </section>

    <!-- Stats -->
    <section class="stats-section">
      <div class="stats-grid">
        <div v-for="stat in stats" :key="stat.label" class="stat-card">
          <span class="stat-icon">{{ stat.icon }}</span>
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </section>

    <!-- Categories -->
    <section class="categories-section">
      <h2 class="section-title">
        <span>🏗️</span> 技能分类
      </h2>
      <div class="categories-grid">
        <RouterLink
          v-for="cat in categories"
          :key="cat.label"
          :to="`/tutorials?category=${cat.label}`"
          class="category-card"
          :style="{ '--cat-color': cat.color }"
        >
          <span class="cat-icon">{{ cat.icon }}</span>
          <span class="cat-name">{{ cat.label }}</span>
          <span class="cat-desc">{{ cat.description }}</span>
          <span class="cat-arrow">→</span>
        </RouterLink>
      </div>
    </section>

    <!-- Featured Tutorials -->
    <section class="tutorials-section">
      <div class="section-header">
        <h2 class="section-title">
          <span>🎬</span> 精品教程
        </h2>
        <RouterLink to="/tutorials" class="section-more">查看全部 →</RouterLink>
      </div>
      <div class="tutorials-grid">
        <RouterLink
          v-for="t in featuredTutorials"
          :key="t.id"
          :to="`/tutorials/${t.id}`"
          class="tutorial-card"
        >
          <div class="tutorial-cover">
            <img :src="t.coverImage" :alt="t.title" />
            <div class="tutorial-overlay">
              <span class="play-btn">▶</span>
            </div>
            <div class="tutorial-difficulty"
              :style="{ background: DIFFICULTY_CONFIG[t.difficulty as keyof typeof DIFFICULTY_CONFIG]?.bgColor, color: DIFFICULTY_CONFIG[t.difficulty as keyof typeof DIFFICULTY_CONFIG]?.color }">
              {{ DIFFICULTY_CONFIG[t.difficulty as keyof typeof DIFFICULTY_CONFIG]?.label }}
            </div>
            <div class="tutorial-duration">⏱ {{ t.duration }}</div>
          </div>
          <div class="tutorial-info">
            <div class="tutorial-category" :style="{ color: CATEGORY_CONFIG[t.category]?.color }">
              {{ CATEGORY_CONFIG[t.category]?.icon }} {{ t.category }}
            </div>
            <h3 class="tutorial-title">{{ t.title }}</h3>
            <p class="tutorial-desc">{{ t.description }}</p>
            <div class="tutorial-meta">
              <span class="tutorial-author">
                <span class="author-avatar" :style="{ background: getAvatarBg(t.author) }">{{ t.author[0] }}</span>
                {{ t.author }}
              </span>
              <span class="tutorial-rating">⭐ {{ t.rating }} ({{ t.reviewCount }})</span>
            </div>
          </div>
        </RouterLink>
      </div>
    </section>

    <!-- How it works -->
    <section class="how-section">
      <h2 class="section-title" style="justify-content:center;">
        <span>💡</span> 如何学习
      </h2>
      <div class="how-grid">
        <div class="how-step">
          <div class="step-number">01</div>
          <div class="step-icon">🎬</div>
          <h3>观看教程</h3>
          <p>选择感兴趣的技能分类，观看视频教程学习基础知识与实操技巧</p>
        </div>
        <div class="how-arrow">→</div>
        <div class="how-step">
          <div class="step-number">02</div>
          <div class="step-icon">📝</div>
          <h3>答题检验</h3>
          <p>完成章节学习后，参加在线答题测试，巩固所学知识</p>
        </div>
        <div class="how-arrow">→</div>
        <div class="how-step">
          <div class="step-number">03</div>
          <div class="step-icon">📸</div>
          <h3>实践上传</h3>
          <p>在生活中实践所学技能，拍照或拍视频上传成果</p>
        </div>
        <div class="how-arrow">→</div>
        <div class="how-step">
          <div class="step-number">04</div>
          <div class="step-icon">🏆</div>
          <h3>获得勋章</h3>
          <p>完成学习、答题和实践任务，获得积分与专属成就勋章</p>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="cta-card">
        <div class="cta-content">
          <h2>准备好开始你的劳动技能学习之旅了吗？</h2>
          <p>加入 thousands of learners，每天进步一点点</p>
          <div class="cta-actions">
            <RouterLink to="/register" class="btn btn-primary btn-lg">免费注册</RouterLink>
            <RouterLink to="/tutorials" class="btn btn-outline btn-lg">随便看看</RouterLink>
          </div>
        </div>
        <div class="cta-decoration">🌱</div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  width: 100%;
}

/* Banner */
.hero-banner {
  position: relative;
  border-radius: var(--radius-xl);
  overflow: hidden;
  margin-bottom: 40px;
  box-shadow: var(--shadow-lg);
}

.banner-slides {
  display: flex;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.banner-slide {
  min-width: 100%;
  height: 420px;
  display: flex;
  align-items: center;
  padding: 0 60px;
  position: relative;
  overflow: hidden;
}

.slide-1 { background: linear-gradient(135deg, #1a4a2e 0%, #2d7a4e 50%, #42b883 100%); }
.slide-2 { background: linear-gradient(135deg, #1a2e4a 0%, #2d5a7a 50%, #3498db 100%); }
.slide-3 { background: linear-gradient(135deg, #4a1a2e 0%, #7a2d5a 50%, #9b59b6 100%); }

.banner-content {
  position: relative;
  z-index: 2;
  max-width: 600px;
}

.banner-tag {
  display: inline-block;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(8px);
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 0.8rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 16px;
  border: 1px solid rgba(255,255,255,0.2);
}

.banner-title {
  font-size: 2.8rem;
  font-weight: 900;
  color: #fff;
  line-height: 1.2;
  margin-bottom: 16px;
}

.banner-desc {
  font-size: 1.05rem;
  color: rgba(255,255,255,0.8);
  margin-bottom: 28px;
}

.banner-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.banner-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 3;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: none;
  background: rgba(255,255,255,0.4);
  cursor: pointer;
  transition: all 0.3s;
}

.dot.active {
  width: 24px;
  border-radius: 4px;
  background: #fff;
}

/* Stats */
.stats-section {
  margin-bottom: 48px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  transition: all 0.25s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  font-size: 2rem;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 900;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.82rem;
  color: var(--text-muted);
}

/* Categories */
.categories-section {
  margin-bottom: 48px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--gap-lg);
}

.section-more {
  font-size: 0.88rem;
  color: var(--primary-color);
  font-weight: 600;
  transition: color 0.2s;
}

.section-more:hover {
  color: var(--primary-color-dark);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.category-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.category-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--cat-color);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  border-color: var(--cat-color);
}

.category-card:hover::before {
  transform: scaleX(1);
}

.cat-icon {
  font-size: 2rem;
  margin-bottom: 4px;
}

.cat-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.cat-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
  line-height: 1.5;
}

.cat-arrow {
  position: absolute;
  bottom: 20px;
  right: 20px;
  font-size: 1.2rem;
  color: var(--cat-color);
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s;
}

.category-card:hover .cat-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* Tutorials */
.tutorials-section {
  margin-bottom: 48px;
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

.tutorial-info {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tutorial-category {
  font-size: 0.78rem;
  font-weight: 600;
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
}

.tutorial-author {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  color: var(--text-secondary);
}

.author-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  color: #fff;
  font-weight: 700;
}

.tutorial-rating {
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* How it works */
.how-section {
  margin-bottom: 48px;
  padding: 48px;
  background: linear-gradient(135deg, rgba(66,184,131,0.04), rgba(52,152,219,0.04));
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
}

.how-grid {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.how-step {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 28px 24px;
  text-align: center;
  width: 200px;
  transition: all 0.3s;
}

.how-step:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.step-number {
  font-size: 0.7rem;
  font-weight: 900;
  color: var(--primary-color);
  opacity: 0.4;
  margin-bottom: 4px;
}

.step-icon {
  font-size: 2.2rem;
  margin-bottom: 8px;
}

.how-step h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.how-step p {
  font-size: 0.78rem;
  color: var(--text-muted);
  line-height: 1.5;
}

.how-arrow {
  font-size: 1.5rem;
  color: var(--primary-color);
  opacity: 0.4;
}

/* CTA */
.cta-section {
  margin-bottom: 32px;
}

.cta-card {
  background: linear-gradient(135deg, #1a4a2e, #2d7a4e);
  border-radius: var(--radius-xl);
  padding: 48px 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.cta-content h2 {
  font-size: 1.8rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 10px;
}

.cta-content p {
  font-size: 1rem;
  color: rgba(255,255,255,0.75);
  margin-bottom: 24px;
}

.cta-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.cta-decoration {
  font-size: 6rem;
  opacity: 0.3;
}

/* Responsive */
@media (max-width: 1024px) {
  .stats-grid,
  .categories-grid,
  .tutorials-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .how-grid {
    gap: 16px;
  }

  .how-arrow {
    display: none;
  }
}

@media (max-width: 768px) {
  .banner-slide {
    height: 320px;
    padding: 0 32px;
  }

  .banner-title {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .cta-card {
    padding: 32px 24px;
  }

  .cta-content h2 {
    font-size: 1.3rem;
  }

  .cta-decoration {
    display: none;
  }

  .how-section {
    padding: 24px;
  }
}
</style>
