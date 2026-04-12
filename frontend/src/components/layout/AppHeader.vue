<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElDropdown, ElDropdownMenu, ElDropdownItem, ElBadge, ElAvatar } from 'element-plus'
import { getAvatarBg } from '@/utils'

const userStore = useUserStore()
const router = useRouter()
const searchKeyword = ref('')
const isMenuOpen = ref(false)

const navLinks = [
  { path: '/', label: '首页' },
  { path: '/tutorials', label: '技能教程' },
  { path: '/quizzes', label: '在线答题' },
  { path: '/tasks', label: '实践任务' },
  { path: '/growth', label: '成长中心' },
]

function handleSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/tutorials', query: { keyword: searchKeyword.value } })
  }
}

function goToProfile() {
  router.push('/profile')
}

function logout() {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  if (userStore.isLoggedIn) {
    userStore.fetchUserInfo()
  }
})
</script>

<template>
  <header class="app-header">
    <div class="header-inner">
      <!-- Logo -->
      <RouterLink to="/" class="logo">
        <div class="logo-icon">🌱</div>
        <div class="logo-text">
          <span class="logo-title">劳动实践平台</span>
          <span class="logo-sub">技能学习与成长</span>
        </div>
      </RouterLink>

      <!-- Desktop Nav -->
      <nav class="desktop-nav">
        <RouterLink
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="nav-link"
          active-class="nav-link--active"
        >
          {{ link.label }}
        </RouterLink>
      </nav>

      <!-- Search -->
      <div class="search-box">
        <input
          v-model="searchKeyword"
          placeholder="搜索教程、题目..."
          class="search-input"
          @keyup.enter="handleSearch"
        />
        <button class="search-btn" @click="handleSearch">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
        </button>
      </div>

      <!-- User Area -->
      <div class="user-area">
        <template v-if="userStore.isLoggedIn">
          <el-badge :value="3" :max="9" class="notif-badge">
            <button class="icon-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
            </button>
          </el-badge>
          <el-dropdown trigger="click" @command="(cmd: string) => cmd === 'profile' ? goToProfile() : logout()">
            <div class="user-info">
              <el-avatar
                :size="36"
                :style="{ background: getAvatarBg(userStore.userInfo?.nickname || 'U') }"
              >
                {{ userStore.userInfo?.nickname?.[0] || 'U' }}
              </el-avatar>
              <div class="user-meta">
                <span class="user-name">{{ userStore.userInfo?.nickname }}</span>
                <span class="user-points">
                  <span class="points-icon">⭐</span>
                  {{ userStore.userInfo?.points || 0 }} 积分
                </span>
              </div>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn btn-ghost">登录</RouterLink>
          <RouterLink to="/register" class="btn btn-primary">注册</RouterLink>
        </template>
      </div>

      <!-- Mobile Toggle -->
      <button class="menu-toggle" @click="isMenuOpen = !isMenuOpen">
        <svg v-if="!isMenuOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide-down">
      <div v-if="isMenuOpen" class="mobile-menu">
        <div class="search-box mobile-search">
          <input v-model="searchKeyword" placeholder="搜索..." class="search-input" @keyup.enter="handleSearch" />
        </div>
        <RouterLink
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="mobile-nav-link"
          @click="isMenuOpen = false"
        >
          {{ link.label }}
        </RouterLink>
      </div>
    </transition>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06);
}

.header-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  font-size: 2rem;
  line-height: 1;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.logo-sub {
  font-size: 0.7rem;
  color: var(--text-muted);
}

.desktop-nav {
  display: flex;
  gap: 4px;
  flex: 1;
}

.nav-link {
  padding: 6px 14px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}

.nav-link:hover {
  color: var(--primary-color);
  background: rgba(66, 184, 131, 0.08);
}

.nav-link--active {
  color: var(--primary-color);
  background: rgba(66, 184, 131, 0.1);
}

.search-box {
  display: flex;
  align-items: center;
  background: var(--bg-soft);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  transition: border-color 0.2s;
  flex-shrink: 0;
}

.search-box:focus-within {
  border-color: var(--primary-color);
}

.search-input {
  border: none;
  background: transparent;
  padding: 8px 14px;
  font-size: 0.875rem;
  color: var(--text-primary);
  width: 200px;
  outline: none;
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-btn {
  padding: 8px 12px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.search-btn:hover {
  color: var(--primary-color);
}

.user-area {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.notif-badge {
  cursor: pointer;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 10px;
  transition: background 0.2s;
}

.user-info:hover {
  background: var(--bg-soft);
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.user-points {
  font-size: 0.72rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 2px;
}

.points-icon {
  font-size: 0.7rem;
}

.btn {
  padding: 7px 16px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
}

.btn-ghost {
  color: var(--text-secondary);
  background: transparent;
}

.btn-ghost:hover {
  color: var(--primary-color);
  background: rgba(66, 184, 131, 0.08);
}

.btn-primary {
  background: var(--primary-color);
  color: #fff;
}

.btn-primary:hover {
  background: #3aa876;
  box-shadow: 0 2px 10px rgba(66, 184, 131, 0.35);
}

.menu-toggle {
  display: none;
  border: none;
  background: transparent;
  color: var(--text-primary);
  cursor: pointer;
  padding: 4px;
}

.mobile-menu {
  padding: 16px 24px;
  background: #fff;
  border-top: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mobile-search {
  margin-bottom: 8px;
  width: 100%;
}

.mobile-search .search-input {
  width: 100%;
}

.mobile-nav-link {
  padding: 10px 14px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: background 0.2s;
}

.mobile-nav-link:hover,
.mobile-nav-link.router-link-active {
  background: rgba(66, 184, 131, 0.08);
  color: var(--primary-color);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.25s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 768px) {
  .desktop-nav,
  .search-box,
  .user-area {
    display: none;
  }
  .menu-toggle {
    display: flex;
  }
  .header-inner {
    gap: 12px;
  }
}
</style>
