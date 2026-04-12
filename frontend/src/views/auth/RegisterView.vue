<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  username: '',
  nickname: '',
  password: '',
  confirmPassword: '',
})
const loading = ref(false)
const agreeTerms = ref(false)

async function handleRegister() {
  if (!form.username || !form.nickname || !form.password) {
    ElMessage.warning('请填写所有必填项')
    return
  }
  if (form.password !== form.confirmPassword) {
    ElMessage.error('两次密码输入不一致')
    return
  }
  if (form.password.length < 6) {
    ElMessage.error('密码至少6位')
    return
  }
  if (!agreeTerms.value) {
    ElMessage.warning('请先同意用户协议')
    return
  }
  loading.value = true
  try {
    await userStore.register({ username: form.username, password: form.password, nickname: form.nickname } as any)
    ElMessage.success('注册成功，欢迎加入！')
    router.push('/')
  } catch (e: any) {
    ElMessage.error(e.message || '注册失败')
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
        <h1>加入我们</h1>
        <p>创建账号，开启你的劳动技能学习之旅</p>
      </div>

      <form class="auth-form" @submit.prevent="handleRegister">
        <div class="form-group">
          <label class="form-label">用户名 <span class="required">*</span></label>
          <div class="input-wrap">
            <span class="input-icon">👤</span>
            <input v-model="form.username" type="text" placeholder="3-20位字母或数字" class="form-input" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">昵称 <span class="required">*</span></label>
          <div class="input-wrap">
            <span class="input-icon">✨</span>
            <input v-model="form.nickname" type="text" placeholder="你的展示名称" class="form-input" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">密码 <span class="required">*</span></label>
          <div class="input-wrap">
            <span class="input-icon">🔒</span>
            <input v-model="form.password" type="password" placeholder="至少6位" class="form-input" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">确认密码 <span class="required">*</span></label>
          <div class="input-wrap">
            <span class="input-icon">🔐</span>
            <input v-model="form.confirmPassword" type="password" placeholder="再输一次密码" class="form-input" />
          </div>
        </div>

        <div class="form-options">
          <label class="checkbox-label">
            <input v-model="agreeTerms" type="checkbox" />
            <span>我已阅读并同意 <a href="#" style="color:var(--primary-color)">《用户协议》</a> 和 <a href="#" style="color:var(--primary-color)">《隐私政策》</a></span>
          </label>
        </div>

        <button type="submit" class="btn btn-primary btn-lg submit-btn" :disabled="loading">
          {{ loading ? '注册中...' : '立即注册' }}
        </button>
      </form>

      <div class="auth-footer">
        已有账号？<RouterLink to="/login">立即登录 →</RouterLink>
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
  gap: 18px;
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

.required {
  color: var(--color-danger);
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

.form-options {
  display: flex;
  align-items: flex-start;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.82rem;
  color: var(--text-secondary);
  cursor: pointer;
  line-height: 1.5;
}

.checkbox-label input {
  margin-top: 3px;
  flex-shrink: 0;
}

.submit-btn {
  width: 100%;
  margin-top: 4px;
}

.auth-footer {
  text-align: center;
  font-size: 0.88rem;
  color: var(--text-muted);
  margin-top: 24px;
}

.auth-footer a {
  color: var(--primary-color);
  font-weight: 600;
  text-decoration: none;
}
</style>
