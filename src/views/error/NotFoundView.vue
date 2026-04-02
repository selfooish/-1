<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="not-found-view">
    <div class="not-found-content">
      <div class="not-found-icon">🔍</div>
      <h1>404</h1>
      <h2>页面不存在</h2>
      <p>抱歉，你访问的页面不存在或已被移除</p>
      <div class="not-found-actions">
        <RouterLink to="/" class="btn btn-primary btn-lg">🏠 返回首页</RouterLink>
        <RouterLink to="/tutorials" class="btn btn-outline btn-lg">🎬 浏览教程</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-view {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.not-found-content {
  text-align: center;
  padding: 40px;
}

.not-found-icon {
  font-size: 5rem;
  margin-bottom: 16px;
}

h1 {
  font-size: 6rem;
  font-weight: 900;
  color: var(--primary-color);
  opacity: 0.2;
  margin-bottom: -20px;
}

h2 {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 12px;
}

p {
  font-size: 0.95rem;
  color: var(--text-muted);
  margin-bottom: 28px;
}

.not-found-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
