<script setup lang="ts">
const footerLinks = [
  { label: '关于我们', path: '/about' },
  { label: '使用帮助', path: '/help' },
  { label: '意见反馈', path: '/feedback' },
  { label: '隐私政策', path: '/privacy' },
]

const categories = ['家电维修', '收纳整理', '绿植养护', '手工制作', '安全常识']
</script>

<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <!-- 品牌区 -->
        <div class="footer-brand">
          <div class="footer-logo">
            <span class="footer-logo-icon">🌱</span>
            <div>
              <div class="footer-logo-title">劳动实践平台</div>
              <div class="footer-logo-sub">技能学习 · 实践成长 · 成就梦想</div>
            </div>
          </div>
          <p class="footer-desc">
            专注劳动技能教育，提供丰富的视频教程、在线题库和实践任务，帮助每一位学习者在劳动中成长。
          </p>
          <div class="social-links">
            <a href="#" class="social-btn" title="微信公众号">📱</a>
            <a href="#" class="social-btn" title="微博">🔔</a>
            <a href="#" class="social-btn" title="抖音">🎵</a>
          </div>
        </div>

        <!-- 技能分类 -->
        <div class="footer-col">
          <h4 class="footer-col-title">技能分类</h4>
          <ul class="footer-links">
            <li v-for="cat in categories" :key="cat">
              <RouterLink :to="`/tutorials?category=${cat}`">{{ cat }}</RouterLink>
            </li>
          </ul>
        </div>

        <!-- 快捷链接 -->
        <div class="footer-col">
          <h4 class="footer-col-title">快捷链接</h4>
          <ul class="footer-links">
            <li><RouterLink to="/tutorials">技能教程</RouterLink></li>
            <li><RouterLink to="/quizzes">在线答题</RouterLink></li>
            <li><RouterLink to="/tasks">实践任务</RouterLink></li>
            <li><RouterLink to="/growth">成长中心</RouterLink></li>
            <li><RouterLink to="/profile">个人中心</RouterLink></li>
          </ul>
        </div>

        <!-- 帮助与反馈 -->
        <div class="footer-col">
          <h4 class="footer-col-title">帮助与支持</h4>
          <ul class="footer-links">
            <li v-for="link in footerLinks" :key="link.path">
              <RouterLink :to="link.path">{{ link.label }}</RouterLink>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© 2025 劳动实践平台 · 让劳动教育更生动</p>
        <div class="footer-badges">
          <span class="footer-badge">🏆 优质教育内容</span>
          <span class="footer-badge">🔒 数据安全</span>
          <span class="footer-badge">♿ 界面无障碍</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: var(--text-primary);
  color: rgba(255, 255, 255, 0.7);
  margin-top: 80px;
}

.footer-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 48px 24px 24px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.footer-brand {}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.footer-logo-icon {
  font-size: 2.4rem;
}

.footer-logo-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
}

.footer-logo-sub {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
}

.footer-desc {
  font-size: 0.85rem;
  line-height: 1.7;
  margin-bottom: 16px;
}

.social-links {
  display: flex;
  gap: 8px;
}

.social-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  text-decoration: none;
  transition: background 0.2s;
}

.social-btn:hover {
  background: rgba(255, 255, 255, 0.15);
}

.footer-col-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 16px;
}

.footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-links a {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: var(--primary-color-light);
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  flex-wrap: wrap;
  gap: 12px;
}

.footer-badges {
  display: flex;
  gap: 12px;
}

.footer-badge {
  background: rgba(255, 255, 255, 0.08);
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  .footer-brand {
    grid-column: 1 / -1;
  }
}

@media (max-width: 480px) {
  .footer-grid {
    grid-template-columns: 1fr;
  }
}
</style>
