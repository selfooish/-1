<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  username: '',
  password: '',
})
const loading = ref(false)
const showPassword = ref(false)

async function handleLogin() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    await userStore.login(form as any)
    ElMessage.success('登录成功，欢迎回来！')
    const redirect = (router.currentRoute.value.query.redirect as string) || '/'
    router.push(redirect)
  } catch (e: any) {
    ElMessage.error(e.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-view">
    <div class="auth-card">
      <div class="auth-header">
        <div class="auth-logo">🌱</div>
        <h1>欢迎回来</h1>
        <p>登录劳动实践平台，继续你的学习之旅</p>
      </div>

      <form class="auth-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <div class="input-wrap">
            <span class="input-icon">👤</span>
            <input
              v-model="form.username"
              type="text"
              placeholder="请输入用户名"
              class="form-input"
              autocomplete="username"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <div class="input-wrap">
            <span class="input-icon">🔒</span>
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="请输入密码"
              class="form-input"
              autocomplete="current-password"
            />
            <button type="button" class="toggle-pwd" @click="showPassword = !showPassword">
              {{ showPassword ? '🙈' : '👁' }}
            </button>
          </div>
        </div>

        <div class="form-options">
          <label class="checkbox-label">
            <input type="checkbox" />
            <span>记住我</span>
          </label>
          <a href="#" class="forgot-link">忘记密码？</a>
        </div>

        <button type="submit" class="btn btn-primary btn-lg submit-btn" :disabled="loading">
          <span v-if="loading">登录中...</span>
          <span v-else>登录</span>
        </button>
      </form>

      <div class="auth-divider">
        <span>或者</span>
      </div>

      <div class="demo-accounts">
        <p class="demo-label">快速体验（演示账号）</p>
        <div class="demo-btns">
          <button class="demo-btn" @click="form.username='student'; form.password='123456'">
            👨‍🎓 学生登录
          </button>
          <button class="demo-btn" @click="form.username='admin'; form.password='123456'">
            👨‍💼 管理员登录
          </button>
        </div>
      </div>

      <div class="auth-footer">
        还没有账号？<RouterLink to="/register">立即注册 →</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-view {
  min-height: calc(100vh - 128px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
  padding: 40px 36px;
  box-shadow: var(--shadow-lg);
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-logo {
  font-size: 3rem;
  margin-bottom: 12px;
}

.auth-header h1 {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.auth-header p {
  font-size: 0.88rem;
  color: var(--text-muted);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.input-wrap {
  display: flex;
  align-items: center;
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: border-color 0.2s;
  background: var(--bg-base);
}

.input-wrap:focus-within {
  border-color: var(--primary-color);
}

.input-icon {
  padding: 0 12px;
  font-size: 1rem;
}

.form-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 8px;
  font-size: 0.9rem;
  color: var(--text-primary);
  outline: none;
}

.form-input::placeholder {
  color: var(--text-muted);
}

.toggle-pwd {
  padding: 0 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1rem;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--text-secondary);
  cursor: pointer;
}

.forgot-link {
  font-size: 0.85rem;
  color: var(--primary-color);
  text-decoration: none;
}

.submit-btn {
  width: 100%;
  margin-top: 4px;
}

.auth-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 24px 0;
  color: var(--text-muted);
  font-size: 0.82rem;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.demo-accounts {
  text-align: center;
  margin-bottom: 24px;
}

.demo-label {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 10px;
}

.demo-btns {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.demo-btn {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-soft);
  color: var(--text-secondary);
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s;
}

.demo-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: var(--primary-bg);
}

.auth-footer {
  text-align: center;
  font-size: 0.88rem;
  color: var(--text-muted);
}

.auth-footer a {
  color: var(--primary-color);
  font-weight: 600;
  text-decoration: none;
}
</style>
