<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { UploadUserFile } from 'element-plus'
import { useTaskStore } from '@/stores/task'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()

const taskId = computed(() => Number(route.params.id))
const task = computed(() => taskStore.currentTask)

const content = ref('')
const fileList = ref<UploadUserFile[]>([])
const submitting = ref(false)

onMounted(() => {
  if (taskId.value) {
    taskStore.fetchTaskDetail(taskId.value)
  }
})

async function handleSubmit() {
  if (content.value.trim().length < 10) {
    ElMessage.warning('请至少填写 10 个字的实践说明')
    return
  }

  if (!fileList.value.length) {
    ElMessage.warning('请至少上传一个附件')
    return
  }

  submitting.value = true
  try {
    const attachments = fileList.value.map((file) => ({
      name: file.name,
      url: `local-upload://${encodeURIComponent(file.name)}`,
      type: file.raw?.type?.startsWith('video/') ? 'video' : 'image',
      size: file.size ?? file.raw?.size ?? 0,
    }))

    await taskStore.submitTask(taskId.value, content.value.trim(), attachments)
    ElMessage.success('任务成果已提交')
    router.push('/my-tasks')
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '提交失败')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="submit-shell">
    <button class="back-btn" @click="router.push(`/tasks/${taskId}`)">返回任务详情</button>

    <div class="submit-card">
      <div class="header-block">
        <p class="eyebrow">Submit</p>
        <h1>{{ task?.title || '提交实践成果' }}</h1>
        <p>这里已经接到 FastAPI `/tasks/:id/submit`，当前为本地附件占位提交流程。</p>
      </div>

      <div class="form-group">
        <label for="task-content">实践说明</label>
        <textarea
          id="task-content"
          v-model="content"
          class="text-area"
          rows="8"
          placeholder="写一下你是怎么完成任务的，遇到了什么问题，最后效果如何。"
        />
      </div>

      <div class="form-group">
        <label>成果附件</label>
        <el-upload
          v-model:file-list="fileList"
          action="#"
          :auto-upload="false"
          list-type="text"
          multiple
        >
          <button type="button" class="btn btn-outline">选择文件</button>
        </el-upload>
      </div>

      <div class="action-row">
        <button class="btn btn-outline" @click="router.push(`/tasks/${taskId}`)">取消</button>
        <button class="btn btn-primary" :disabled="submitting" @click="handleSubmit">
          {{ submitting ? '提交中...' : '确认提交' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.submit-shell {
  max-width: 860px;
  margin: 0 auto;
}

.back-btn {
  margin-bottom: 16px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
}

.submit-card {
  padding: 24px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.header-block {
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--primary-color);
}

.header-block h1 {
  margin: 0 0 8px;
  color: var(--text-primary);
  font-size: 30px;
}

.header-block p {
  margin: 0;
  color: var(--text-muted);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.form-group label {
  color: var(--text-primary);
  font-weight: 700;
}

.text-area {
  width: 100%;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-base);
  color: var(--text-primary);
  resize: vertical;
  font: inherit;
}

.action-row {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
