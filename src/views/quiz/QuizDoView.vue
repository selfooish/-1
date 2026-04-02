<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const quizId = Number(route.params.id)

// 模拟题目数据
const questions = ref([
  {
    id: 1,
    type: 'single',
    stem: '电饭煲不通电，最先应该检查哪个部件？',
    options: [
      { label: 'A', text: '加热盘' },
      { label: 'B', text: '电源线和插头' },
      { label: 'C', text: '温度传感器' },
      { label: 'D', text: '控制板' },
    ],
    answer: 'B',
    explanation: '电饭煲不通电时，应首先检查电源线和插头是否连接正常，这是最常见的故障原因。',
  },
  {
    id: 2,
    type: 'multiple',
    stem: '以下哪些方法可以延长绿萝的养护寿命？（多选）',
    options: [
      { label: 'A', text: '避免阳光直射' },
      { label: 'B', text: '保持土壤湿润但不过涝' },
      { label: 'C', text: '每周施加大量化肥' },
      { label: 'D', text: '定期擦拭叶片' },
    ],
    answer: ['A', 'B', 'D'],
    explanation: '绿萝喜阴，避免阳光直射；喜湿润但不耐涝；每周施大量化肥会烧根；擦拭叶片有助于光合作用。',
  },
  {
    id: 3,
    type: 'judge',
    stem: '用完熨斗后，可以立即将熨斗放入抽屉中储存。',
    options: [
      { label: '√', text: '正确' },
      { label: '×', text: '错误' },
    ],
    answer: '×',
    explanation: '熨斗使用后底板温度很高，必须等完全冷却后再收纳，以免引发火灾或损坏衣物。',
  },
  {
    id: 4,
    type: 'single',
    stem: '衣柜收纳时，应该将常穿的衣服放在哪一层？',
    options: [
      { label: 'A', text: '最底层' },
      { label: 'B', text: '中间层（视线平行处）' },
      { label: 'C', text: '最顶层' },
      { label: 'D', text: '抽屉里' },
    ],
    answer: 'B',
    explanation: '将常穿的衣服放在视线平行处（中间层），拿取最方便，节省时间。',
  },
  {
    id: 5,
    type: 'single',
    stem: '家庭手工制作中，以下哪种材料属于可回收再利用？',
    options: [
      { label: 'A', text: '塑料袋' },
      { label: 'B', text: '旧衣物' },
      { label: 'C', text: '一次性泡沫餐盒' },
      { label: 'D', text: '金属罐头' },
    ],
    answer: 'B',
    explanation: '旧衣物可以通过裁剪、缝制变成布艺收纳袋、抹布等，属于可回收再利用的材料。',
  },
])

const currentIdx = ref(0)
const answers = ref<Record<number, string | string[]>>({})
const timeLeft = ref(20 * 60) // 20 分钟
const isSubmitted = ref(false)
const results = ref<any[]>([])
let timer: ReturnType<typeof setInterval> | null = null

const currentQuestion = computed(() => questions.value[currentIdx.value])
const answeredCount = computed(() => Object.keys(answers.value).length)
const progress = computed(() => `${(answeredCount.value / questions.value.length) * 100}%`)

function selectAnswer(label: string) {
  const q = currentQuestion.value
  if (q.type === 'multiple') {
    const current = (answers.value[q.id] as string[]) || []
    if (current.includes(label)) {
      answers.value[q.id] = current.filter(l => l !== label)
    } else {
      answers.value[q.id] = [...current, label]
    }
  } else {
    answers.value[q.id] = label
  }
}

function isSelected(label: string): boolean {
  const ans = answers.value[currentQuestion.value.id]
  if (Array.isArray(ans)) return ans.includes(label)
  return ans === label
}

function submitQuiz() {
  if (timer) clearInterval(timer)
  isSubmitted.value = true
  results.value = questions.value.map(q => ({
    ...q,
    userAnswer: answers.value[q.id],
    isCorrect: JSON.stringify(answers.value[q.id]) === JSON.stringify(q.answer),
  }))
  const correct = results.value.filter(r => r.isCorrect).length
  const score = Math.round((correct / questions.value.length) * 100)
  if (score >= 60) {
    ElMessage.success(`🎉 答题完成！得分 ${score} 分，恭喜及格！`)
  } else {
    ElMessage.warning(`答题完成！得分 ${score} 分，未达及格线，继续加油！`)
  }
}

function formatTime(s: number) {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`
}

onMounted(() => {
  timer = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      submitQuiz()
    }
  }, 1000)
})

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="quiz-do-view">
    <!-- 顶部状态栏 -->
    <div class="quiz-topbar">
      <button class="back-btn" @click="router.push(`/quizzes/${quizId}`)">← 返回</button>
      <div class="quiz-progress">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress }" />
        </div>
        <span class="progress-text">{{ answeredCount }}/{{ questions.length }} 已答</span>
      </div>
      <div class="timer" :class="{ warning: timeLeft < 300 }">
        ⏱ {{ formatTime(timeLeft) }}
      </div>
    </div>

    <!-- 答题区域 -->
    <div v-if="!isSubmitted" class="quiz-content">
      <div class="question-card">
        <div class="question-header">
          <span class="q-number">{{ currentIdx + 1 }} / {{ questions.length }}</span>
          <span class="q-type">
            {{ currentQuestion.type === 'single' ? '单选题' : currentQuestion.type === 'multiple' ? '多选题' : currentQuestion.type === 'judge' ? '判断题' : '问答题' }}
          </span>
        </div>
        <h2 class="question-stem">{{ currentQuestion.stem }}</h2>
        <div class="options-list">
          <button
            v-for="opt in currentQuestion.options"
            :key="opt.label"
            class="option-btn"
            :class="{ selected: isSelected(opt.label) }"
            @click="selectAnswer(opt.label)"
          >
            <span class="option-label">{{ opt.label }}</span>
            <span class="option-text">{{ opt.text }}</span>
          </button>
        </div>
      </div>

      <!-- 题目导航 -->
      <div class="question-nav">
        <button
          v-for="(q, idx) in questions"
          :key="q.id"
          class="q-nav-btn"
          :class="{
            active: idx === currentIdx,
            answered: answers[q.id] !== undefined,
          }"
          @click="currentIdx = idx"
        >
          {{ idx + 1 }}
        </button>
      </div>

      <div class="quiz-actions">
        <button class="btn btn-outline" :disabled="currentIdx === 0" @click="currentIdx--">← 上一题</button>
        <button
          v-if="currentIdx < questions.length - 1"
          class="btn btn-primary"
          @click="currentIdx++"
        >
          下一题 →
        </button>
        <button
          v-else
          class="btn btn-primary btn-lg"
          :disabled="answeredCount < questions.length"
          @click="submitQuiz"
        >
          提交测验 {{ answeredCount < questions.length ? `(${answeredCount}/${questions.length})` : '' }}
        </button>
      </div>
    </div>

    <!-- 结果区域 -->
    <div v-else class="results-view">
      <div class="results-header">
        <div class="results-icon">🏆</div>
        <h2>答题完成！</h2>
        <p>你已完成本次测验</p>
      </div>

      <div class="result-list">
        <div
          v-for="r in results"
          :key="r.id"
          class="result-item"
          :class="{ correct: r.isCorrect, wrong: !r.isCorrect }"
        >
          <div class="result-header">
            <span class="result-icon">{{ r.isCorrect ? '✅' : '❌' }}</span>
            <span class="result-stem">{{ r.stem }}</span>
          </div>
          <div class="result-answer">
            <span>你的答案: {{ Array.isArray(r.userAnswer) ? r.userAnswer.join(',') : r.userAnswer || '未作答' }}</span>
            <span v-if="!r.isCorrect">正确答案: {{ Array.isArray(r.answer) ? r.answer.join(',') : r.answer }}</span>
          </div>
          <div class="result-explanation">
            💡 {{ r.explanation }}
          </div>
        </div>
      </div>

      <div class="results-actions">
        <button class="btn btn-primary btn-lg" @click="router.push('/quizzes')">返回题库</button>
        <button class="btn btn-outline btn-lg" @click="router.push(`/quizzes/${quizId}`)">查看详情</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiz-do-view {
  max-width: 900px;
  margin: 0 auto;
}

.quiz-topbar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  margin-bottom: 24px;
  position: sticky;
  top: 80px;
  z-index: 10;
}

.back-btn {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.85rem;
  cursor: pointer;
  transition: color 0.2s;
  flex-shrink: 0;
}

.back-btn:hover {
  color: var(--primary-color);
}

.quiz-progress {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: var(--bg-soft);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary-color);
  border-radius: 3px;
  transition: width 0.3s;
}

.progress-text {
  font-size: 0.78rem;
  color: var(--text-muted);
  white-space: nowrap;
}

.timer {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  background: var(--bg-soft);
  padding: 6px 14px;
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.timer.warning {
  background: rgba(231, 76, 60, 0.1);
  color: var(--color-danger);
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.quiz-content {}

.question-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 20px;
}

.question-header {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.q-number {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--primary-color);
  background: rgba(66, 184, 131, 0.1);
  padding: 2px 10px;
  border-radius: 20px;
}

.q-type {
  font-size: 0.8rem;
  color: var(--text-muted);
  background: var(--bg-soft);
  padding: 2px 10px;
  border-radius: 20px;
}

.question-stem {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.6;
  margin-bottom: 24px;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-base);
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  font-size: 0.9rem;
}

.option-btn:hover {
  border-color: var(--primary-color);
  background: rgba(66, 184, 131, 0.04);
}

.option-btn.selected {
  border-color: var(--primary-color);
  background: rgba(66, 184, 131, 0.1);
  color: var(--primary-color);
}

.option-label {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.option-btn.selected .option-label {
  background: var(--primary-color);
  color: #fff;
}

.option-text {
  flex: 1;
  color: var(--text-primary);
  line-height: 1.5;
}

.question-nav {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.q-nav-btn {
  width: 36px;
  height: 36px;
  border: 1.5px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-card);
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.q-nav-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.q-nav-btn.answered {
  border-color: var(--primary-color);
  background: rgba(66, 184, 131, 0.1);
  color: var(--primary-color);
}

.q-nav-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: #fff;
}

.quiz-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

/* Results */
.results-view {}

.results-header {
  text-align: center;
  margin-bottom: 32px;
}

.results-icon {
  font-size: 4rem;
  margin-bottom: 12px;
}

.results-header h2 {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.results-header p {
  color: var(--text-muted);
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
}

.result-item {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
  border-left: 4px solid;
}

.result-item.correct {
  border-left-color: var(--color-success);
  background: rgba(39, 174, 96, 0.02);
}

.result-item.wrong {
  border-left-color: var(--color-danger);
  background: rgba(231, 76, 60, 0.02);
}

.result-header {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
}

.result-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.result-stem {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.5;
}

.result-answer {
  display: flex;
  gap: 16px;
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.result-answer span:last-child {
  color: var(--color-success);
  font-weight: 600;
}

.result-item.wrong .result-answer span:last-child {
  color: var(--color-danger);
}

.result-explanation {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.6;
  padding: 10px;
  background: rgba(0,0,0,0.03);
  border-radius: var(--radius-md);
}

.results-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}
</style>
