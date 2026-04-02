<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElUpload } from 'element-plus'
import type { UploadFile } from 'element-plus'

const route = useRoute()
const router = useRouter()
const taskId = Number(route.params.id)

const content = ref('')
const fileList = ref<UploadFile[]>([])
const submitting = ref(false)

async function handleSubmit() {
  if (!content.value.trim()) {
    ElMessage.warning('请填写实践心得')
    return
  }
  if (fileList.value.length === 0) {
    ElMessage.warning('请至少上传一张照片')
    return
  }
  submitting.value = true
  try {
    await new Promise(r => setTimeout(r, 1500))
    ElMessage.success('🎉 成果提交成功！请等待评委审核')
    router.push('/my-tasks')
  } catch {
    ElMessage.error('提交失败，请重试')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="task-submit-view">
    <button class="back-btn" @click="router.push(`/tasks/${taskId}`)">← 返回任务详情</button>

    <div class="submit-card">
      <div class="submit-header">
        <h1>📤 提交实践成果</h1>
        <p>记录你的劳动实践过程，上传照片或视频</p>
      </div>

      <div class="form-section">
        <label class="form-label">实践心得 <span class="required">*</span></label>
        <textarea
          v-model="content"
          class="form-textarea"
          placeholder="请描述你的实践过程、遇到的困难、解决方法以及收获...（至少50字）"
          rows="6"
        />
        <div class="char-count" :class="{ ok: content.length >= 50 }">
          {{ content.length }} / 50 字以上
        </div>
      </div>

      <div class="form-section">
        <label class="form-label">上传照片/视频 <span class="required">*</span></label>
        <el-upload
          v-model:file-list="fileList"
          action="#"
          :auto-upload="false"
          :limit="6"
          accept="image/*,video/*"
          list-type="picture-card"
        >
          <div class="upload-trigger">
            <span class="upload-icon">+</span>
            <span class="upload-text">点击上传</span>
          </div>
        </el-upload>
        <p class="upload-hint">支持 JPG、PNG 图片和 MP4 视频，最多 6 个文件</p>
      </div>

      <div class="submit-actions">
        <button class="btn btn-outline" @click="router.push(`/tasks/${taskId}`)">取消</button>
        <button class="btn btn-primary btn-lg" :disabled="submitting || content.length < 50 || fileList.length === 0" @click="handleSubmit">
          {{ submitting ? '提交中...' : '✅ 提交成果' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task-submit-view { max-width: 720px; margin: 0 auto; }
.back-btn { border: none; background: transparent; color: var(--text-secondary); font-size: 0.85rem; cursor: pointer; margin-bottom: 20px; padding: 0; transition: color 0.2s; }
.back-btn:hover { color: var(--primary-color); }
.submit-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-xl); padding: 32px; }
.submit-header { margin-bottom: 28px; }
.submit-header h1 { font-size: 1.4rem; font-weight: 800; color: var(--text-primary); margin-bottom: 6px; }
.submit-header p { font-size: 0.88rem; color: var(--text-muted); }
.form-section { margin-bottom: 24px; }
.form-label { display: block; font-size: 0.9rem; font-weight: 600; color: var(--text-primary); margin-bottom: 10px; }
.required { color: var(--color-danger); }
.form-textarea { width: 100%; padding: 14px 16px; border: 1.5px solid var(--border-color); border-radius: var(--radius-md); font-size: 0.9rem; color: var(--text-primary); background: var(--bg-base); resize: vertical; outline: none; transition: border-color 0.2s; line-height: 1.6; font-family: inherit; }
.form-textarea:focus { border-color: var(--primary-color); }
.form-textarea::placeholder { color: var(--text-muted); }
.char-count { font-size: 0.75rem; color: var(--text-muted); text-align: right; margin-top: 6px; }
.char-count.ok { color: var(--color-success); }
.upload-trigger { width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; }
.upload-icon { font-size: 1.5rem; color: var(--text-muted); }
.upload-text { font-size: 0.7rem; color: var(--text-muted); }
.upload-hint { font-size: 0.75rem; color: var(--text-muted); margin-top: 8px; }
.submit-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 28px; }
</style>
