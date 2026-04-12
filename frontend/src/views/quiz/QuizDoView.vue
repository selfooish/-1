<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useQuizStore } from '@/stores/quiz'

const route = useRoute()
const router = useRouter()
const quizStore = useQuizStore()

const quizId = computed(() => Number(route.params.id))
const quiz = computed(() => quizStore.currentQuiz)
const questions = computed(() => quizStore.questions)
const loading = computed(() => quizStore.loading)

const currentIndex = ref(0)
const answers = ref<Record<number, string | string[]>>({})
const timeLeft = ref(0)
const submitted = ref(false)
const submitting = ref(false)
const resultScore = ref<number | null>(null)
const resultCorrectCount = ref<number | null>(null)

let timer: ReturnType<typeof setInterval> | null = null

const currentQuestion = computed(() => questions.value[currentIndex.value])
const answeredCount = computed(() => Object.keys(answers.value).length)

function resetTimer(minutes: number) {
  if (timer) clearInterval(timer)
  timeLeft.value = minutes * 60
  timer = setInterval(() => {
    timeLeft.value -= 1
    if (timeLeft.value <= 0) {
      submitQuiz()
    }
  }, 1000)
}

function formatTime(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

function selectOption(label: string) {
  const question = currentQuestion.value
  if (!question) return

  if (question.type === 'multiple') {
    const current = Array.isArray(answers.value[question.id]) ? [...(answers.value[question.id] as string[])] : []
    const next = current.includes(label) ? current.filter((item) => item !== label) : [...current, label]
    answers.value[question.id] = next
    return
  }

  answers.value[question.id] = label
}

function isSelected(label: string) {
  const question = currentQuestion.value
  if (!question) return false
  const value = answers.value[question.id]
  return Array.isArray(value) ? value.includes(label) : value === label
}

async function loadQuiz() {
  await quizStore.fetchQuizDetail(quizId.value)
  if (quiz.value) {
    resetTimer(quiz.value.timeLimit)
  }
}

async function submitQuiz() {
  if (submitted.value || submitting.value || !quiz.value) return

  submitting.value = true
  try {
    const record = await quizStore.submitQuiz(quiz.value.id, answers.value)
    resultScore.value = record.score
    resultCorrectCount.value = record.correctCount
    submitted.value = true
    if (timer) clearInterval(timer)
    ElMessage.success('答题已提交')
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '提交失败')
  } finally {
    submitting.value = false
  }
}

watch(
  () => quiz.value?.timeLimit,
  (minutes) => {
    if (minutes && !submitted.value) {
      resetTimer(minutes)
    }
  }
)

onMounted(loadQuiz)

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="quiz-shell">
    <div class="topbar">
      <button class="back-btn" @click="router.push(`/quizzes/${quizId}`)">返回</button>
      <div class="progress-text">已答 {{ answeredCount }}/{{ questions.length }}</div>
      <div class="timer">{{ formatTime(timeLeft) }}</div>
    </div>

    <div v-if="loading" class="state-card">正在加载题目...</div>

    <div v-else-if="submitted" class="result-card">
      <h1>答题完成</h1>
      <p>得分：{{ resultScore ?? 0 }} / {{ quiz?.totalScore ?? 0 }}</p>
      <p>答对：{{ resultCorrectCount ?? 0 }} / {{ questions.length }}</p>
      <div class="result-actions">
        <button class="btn btn-primary" @click="router.push('/quizzes')">返回题库</button>
        <button class="btn btn-outline" @click="router.push(`/quizzes/${quizId}`)">查看详情</button>
      </div>
    </div>

    <div v-else-if="quiz && currentQuestion" class="quiz-layout">
      <section class="question-card">
        <div class="question-header">
          <span>第 {{ currentIndex + 1 }} 题 / 共 {{ questions.length }} 题</span>
          <span>{{ currentQuestion.type }}</span>
        </div>

        <h1 class="question-title">{{ currentQuestion.stem }}</h1>

        <div class="option-list">
          <button
            v-for="option in currentQuestion.options || []"
            :key="option.label"
            class="option-item"
            :class="{ selected: isSelected(option.label) }"
            @click="selectOption(option.label)"
          >
            <span class="option-label">{{ option.label }}</span>
            <span>{{ option.text }}</span>
          </button>
        </div>

        <div class="action-row">
          <button class="btn btn-outline" :disabled="currentIndex === 0" @click="currentIndex -= 1">
            上一题
          </button>
          <button
            v-if="currentIndex < questions.length - 1"
            class="btn btn-primary"
            @click="currentIndex += 1"
          >
            下一题
          </button>
          <button v-else class="btn btn-primary" :disabled="submitting" @click="submitQuiz">
            {{ submitting ? '提交中...' : '提交答卷' }}
          </button>
        </div>
      </section>

      <aside class="nav-card">
        <h3>题号导航</h3>
        <div class="nav-grid">
          <button
            v-for="(question, index) in questions"
            :key="question.id"
            class="nav-item"
            :class="{
              active: index === currentIndex,
              answered: answers[question.id] !== undefined,
            }"
            @click="currentIndex = index"
          >
            {{ index + 1 }}
          </button>
        </div>
      </aside>
    </div>

    <div v-else class="state-card">没有加载到题目。</div>
  </div>
</template>

<style scoped>
.quiz-shell {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.back-btn {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
}

.progress-text {
  flex: 1;
  color: var(--text-muted);
}

.timer {
  font-weight: 700;
  color: var(--text-primary);
}

.quiz-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 20px;
}

.question-card,
.nav-card,
.state-card,
.result-card {
  padding: 20px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}

.question-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
  color: var(--text-muted);
}

.question-title {
  margin: 0 0 20px;
  color: var(--text-primary);
  font-size: 26px;
  line-height: 1.5;
}

.option-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-base);
  color: var(--text-primary);
  text-align: left;
  cursor: pointer;
}

.option-item.selected {
  border-color: var(--primary-color);
  background: rgba(66, 184, 131, 0.08);
}

.option-label {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--bg-soft);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.action-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 20px;
}

.nav-card h3 {
  margin: 0 0 14px;
  color: var(--text-primary);
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.nav-item {
  aspect-ratio: 1;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background: var(--bg-base);
  color: var(--text-muted);
  cursor: pointer;
}

.nav-item.active {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.nav-item.answered {
  background: rgba(66, 184, 131, 0.08);
}

.state-card,
.result-card {
  text-align: center;
  color: var(--text-muted);
}

.result-card h1 {
  margin: 0 0 12px;
  color: var(--text-primary);
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
}

@media (max-width: 960px) {
  .quiz-layout {
    grid-template-columns: 1fr;
  }
}
</style>
