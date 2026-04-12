import bcrypt from 'bcryptjs'
import { calcLevel, toIso } from '../shared/utils.js'
import type { UserRole } from '../shared/auth.js'

type TutorialCategory =
  | '家电维修'
  | '收纳整理'
  | '绿植养护'
  | '手工制作'
  | '安全常识'
  | '烹饪基础'
  | '衣物护理'
  | '清洁卫生'

type Difficulty = 'easy' | 'medium' | 'hard'

type UserRecord = {
  id: number
  username: string
  nickname: string
  passwordHash: string
  avatar: string
  role: UserRole
  points: number
  email?: string
  phone?: string
  bio?: string
  createdAt: string
}

type TutorialRecord = {
  id: number
  title: string
  category: TutorialCategory
  coverImage: string
  description: string
  duration: string
  difficulty: Difficulty
  author: string
  authorAvatar: string
  viewCount: number
  collectCount: number
  tags: string[]
  rating: number
  reviewCount: number
  createdAt: string
  updatedAt: string
  chapters: Array<{
    id: number
    title: string
    duration: string
    isFree: boolean
    videoUrl?: string
  }>
}

type TaskRecord = {
  id: number
  title: string
  description: string
  category: TutorialCategory
  coverImage: string
  points: number
  difficulty: Difficulty
  deadline: string
  maxSubmits: number
  createdAt: string
}

type QuizRecordSeed = {
  id: number
  title: string
  description: string
  questionCount: number
  timeLimit: number
  passScore: number
  totalScore: number
  category: TutorialCategory | '综合'
  difficulty: Difficulty
  tags: string[]
  createdAt: string
}

type QuestionRecord = {
  id: number
  quizId: number
  type: 'single' | 'multiple' | 'judge'
  stem: string
  options: Array<{ label: string; text: string }>
  answer: string | string[]
  explanation: string
  difficulty: Difficulty
  category: string
  tags: string[]
}

type TaskSubmissionRecord = {
  id: number
  taskId: number
  userId: number
  content: string
  attachments: Array<{ name: string; url: string; type: 'image' | 'video' | 'document'; size: number }>
  submittedAt: string
  status: 'pending' | 'approved' | 'rejected'
  points?: number
  reviewerComment?: string
}

type QuizSubmitRecord = {
  id: number
  quizId: number
  userId: number
  score: number
  totalScore: number
  correctCount: number
  totalQuestions: number
  timeSpent: number
  submittedAt: string
  answers: Array<{
    questionId: number
    userAnswer: string | string[]
    isCorrect: boolean
    score: number
  }>
}

export const users: UserRecord[] = [
  {
    id: 1,
    username: 'student',
    nickname: '小明',
    passwordHash: bcrypt.hashSync('123456', 10),
    avatar: '',
    role: 'student',
    points: 850,
    email: 'xiaoming@example.com',
    phone: '13800000000',
    bio: '热爱劳动，喜欢动手实践。',
    createdAt: toIso('2025-01-01'),
  },
  {
    id: 2,
    username: 'admin',
    nickname: '管理员',
    passwordHash: bcrypt.hashSync('123456', 10),
    avatar: '',
    role: 'admin',
    points: 1800,
    createdAt: toIso('2025-01-01'),
  },
]

export const tutorials: TutorialRecord[] = [
  {
    id: 1,
    title: '电饭煲常见故障与维修',
    category: '家电维修',
    coverImage: 'https://picsum.photos/seed/tutorial-1/800/450',
    description: '从拆解到排查，帮助学生理解常见家电维修的安全流程和基本方法。',
    duration: '2h30m',
    difficulty: 'medium',
    author: '王老师',
    authorAvatar: '',
    viewCount: 2341,
    collectCount: 156,
    tags: ['家电维修', '安全第一', '动手实践'],
    rating: 4.8,
    reviewCount: 156,
    createdAt: toIso('2025-01-10'),
    updatedAt: toIso('2025-02-10'),
    chapters: [
      { id: 1, title: '基本结构', duration: '15:00', isFree: true, videoUrl: '' },
      { id: 2, title: '常见故障', duration: '20:00', isFree: true, videoUrl: '' },
      { id: 3, title: '不通电排查', duration: '25:00', isFree: false, videoUrl: '' },
    ],
  },
  {
    id: 2,
    title: '衣柜收纳全攻略',
    category: '收纳整理',
    coverImage: 'https://picsum.photos/seed/tutorial-2/800/450',
    description: '理解分类、折叠、分层和长期维护的方法。',
    duration: '1h15m',
    difficulty: 'easy',
    author: '李老师',
    authorAvatar: '',
    viewCount: 4102,
    collectCount: 289,
    tags: ['收纳', '整理', '空间利用'],
    rating: 4.9,
    reviewCount: 289,
    createdAt: toIso('2025-01-12'),
    updatedAt: toIso('2025-02-12'),
    chapters: [
      { id: 4, title: '衣物分类', duration: '10:00', isFree: true, videoUrl: '' },
      { id: 5, title: '折叠方法', duration: '18:00', isFree: true, videoUrl: '' },
      { id: 6, title: '长期维护', duration: '12:00', isFree: false, videoUrl: '' },
    ],
  },
]

export const tasks: TaskRecord[] = [
  {
    id: 1,
    title: '完成一次电饭煲清洁与维护',
    description: '记录清洁前后对比和清洁心得。',
    category: '家电维修',
    coverImage: 'https://picsum.photos/seed/task-1/800/450',
    points: 50,
    difficulty: 'easy',
    deadline: toIso('2026-05-01'),
    maxSubmits: 1,
    createdAt: toIso('2025-01-15'),
  },
  {
    id: 2,
    title: '整理衣柜并提交分类记录',
    description: '按季节和使用频率进行分类整理。',
    category: '收纳整理',
    coverImage: 'https://picsum.photos/seed/task-2/800/450',
    points: 40,
    difficulty: 'easy',
    deadline: toIso('2026-05-10'),
    maxSubmits: 1,
    createdAt: toIso('2025-01-18'),
  },
]

export const quizzes: QuizRecordSeed[] = [
  {
    id: 1,
    title: '家电维修基础知识测验',
    description: '检验常见家电故障排查与安全操作知识。',
    questionCount: 3,
    timeLimit: 20,
    passScore: 60,
    totalScore: 100,
    category: '家电维修',
    difficulty: 'easy',
    tags: ['家电维修', '基础'],
    createdAt: toIso('2025-01-20'),
  },
]

export const questions: QuestionRecord[] = [
  {
    id: 1,
    quizId: 1,
    type: 'single',
    stem: '电饭煲不通电时，优先检查哪一项？',
    options: [
      { label: 'A', text: '加热盘' },
      { label: 'B', text: '电源线和插头' },
      { label: 'C', text: '温度传感器' },
      { label: 'D', text: '控制板' },
    ],
    answer: 'B',
    explanation: '先检查电源线和插头是否正常，是最基础也最常见的排查步骤。',
    difficulty: 'easy',
    category: '家电维修',
    tags: ['基础'],
  },
  {
    id: 2,
    quizId: 1,
    type: 'multiple',
    stem: '以下哪些做法有助于家电清洁安全？',
    options: [
      { label: 'A', text: '断电后再拆洗' },
      { label: 'B', text: '手湿时操作插头' },
      { label: 'C', text: '等待部件冷却' },
      { label: 'D', text: '阅读说明书' },
    ],
    answer: ['A', 'C', 'D'],
    explanation: '安全前提包括断电、冷却和按说明操作。',
    difficulty: 'easy',
    category: '家电维修',
    tags: ['安全'],
  },
  {
    id: 3,
    quizId: 1,
    type: 'judge',
    stem: '设备刚断电时可以立即清洗内部发热部件。',
    options: [
      { label: 'T', text: '正确' },
      { label: 'F', text: '错误' },
    ],
    answer: 'F',
    explanation: '需要等待冷却，避免烫伤和损坏设备。',
    difficulty: 'easy',
    category: '家电维修',
    tags: ['安全'],
  },
]

export const collections = new Set<string>(['1:1'])
export const completedChapters = new Set<string>(['1:1'])

export const taskSubmissions: TaskSubmissionRecord[] = [
  {
    id: 1,
    taskId: 1,
    userId: 1,
    content: '我完成了电饭煲清洁，并记录了清洁前后的变化。',
    attachments: [
      {
        name: 'before-after.jpg',
        url: 'https://picsum.photos/seed/submission-1/600/400',
        type: 'image',
        size: 102400,
      },
    ],
    submittedAt: toIso('2025-02-01'),
    status: 'approved',
    points: 50,
    reviewerComment: '记录清晰，步骤完整。',
  },
]

export const quizRecords: QuizSubmitRecord[] = [
  {
    id: 1,
    quizId: 1,
    userId: 1,
    score: 85,
    totalScore: 100,
    correctCount: 2,
    totalQuestions: 3,
    timeSpent: 420,
    submittedAt: toIso('2025-02-02'),
    answers: [
      { questionId: 1, userAnswer: 'B', isCorrect: true, score: 35 },
      { questionId: 2, userAnswer: ['A', 'C'], isCorrect: false, score: 0 },
      { questionId: 3, userAnswer: 'F', isCorrect: true, score: 50 },
    ],
  },
]

export const pointRecords = [
  { id: 1, userId: 1, type: 'tutorial', action: '完成教程《电饭煲常见故障与维修》', points: 30, createdAt: toIso('2025-02-01') },
  { id: 2, userId: 1, type: 'quiz', action: '完成测验《家电维修基础知识测验》', points: 50, createdAt: toIso('2025-02-02') },
  { id: 3, userId: 1, type: 'task', action: '任务《完成一次电饭煲清洁与维护》审核通过', points: 80, createdAt: toIso('2025-02-03') },
]

export const badges = [
  { id: 1, name: '初学者', description: '完成第一个教程', icon: '🌱', color: '#42b883', type: 'skill', requirement: '完成1个教程', unlockedAt: toIso('2025-02-01'), progress: 1, total: 1 },
  { id: 2, name: '答题达人', description: '完成10次答题', icon: '📝', color: '#3498db', type: 'quiz', requirement: '完成10次答题', unlockedAt: undefined, progress: 3, total: 10 },
]

export const growthDays = Array.from({ length: 30 }, (_, index) => ({
  date: toIso(new Date(Date.now() - (29 - index) * 24 * 60 * 60 * 1000)).slice(0, 10),
  points: (index % 5) * 20,
  tasksCompleted: index % 3 === 0 ? 1 : 0,
  tutorialsCompleted: index % 4 === 0 ? 1 : 0,
  quizzesTaken: index % 2 === 0 ? 1 : 0,
}))

export function findUserById(userId: number) {
  return users.find((user) => user.id === userId)
}

export function findUserByUsername(username: string) {
  return users.find((user) => user.username === username)
}

export function publicUser(user: UserRecord) {
  const level = calcLevel(user.points)
  return {
    id: user.id,
    username: user.username,
    nickname: user.nickname,
    avatar: user.avatar,
    role: user.role,
    points: user.points,
    level: level.level,
    title: level.title,
    createdAt: user.createdAt,
    email: user.email || '',
    phone: user.phone || '',
    bio: user.bio || '',
  }
}

export function tutorialForUser(tutorial: TutorialRecord, userId?: number) {
  return {
    ...tutorial,
    isCollected: userId ? collections.has(`${userId}:${tutorial.id}`) : false,
    isPurchased: true,
    chapters: tutorial.chapters.map((chapter) => ({
      ...chapter,
      isCompleted: userId ? completedChapters.has(`${userId}:${chapter.id}`) : false,
    })),
  }
}

export function tutorialListItemForUser(tutorial: TutorialRecord, userId?: number) {
  const detail = tutorialForUser(tutorial, userId)
  return {
    id: detail.id,
    title: detail.title,
    category: detail.category,
    coverImage: detail.coverImage,
    description: detail.description,
    duration: detail.duration,
    difficulty: detail.difficulty,
    author: detail.author,
    viewCount: detail.viewCount,
    collectCount: detail.collectCount,
    rating: detail.rating,
    reviewCount: detail.reviewCount,
    isCollected: detail.isCollected,
  }
}

export function taskForUser(task: TaskRecord, userId?: number) {
  const userSubmissionList = taskSubmissions.filter((item) => item.taskId === task.id && item.userId === userId)
  const latest = userSubmissionList[0]

  let status: 'pending' | 'in_progress' | 'submitted' | 'reviewed' = 'pending'
  let reviewStatus: 'excellent' | 'pass' | 'fail' | undefined
  let reviewerComment: string | undefined

  if (latest) {
    status = latest.status === 'pending' ? 'submitted' : 'reviewed'
    if (latest.status === 'approved') {
      reviewStatus = latest.points && latest.points >= task.points ? 'excellent' : 'pass'
    }
    if (latest.status === 'rejected') {
      reviewStatus = 'fail'
    }
    reviewerComment = latest.reviewerComment
  }

  return {
    ...task,
    status,
    submitCount: userSubmissionList.length,
    maxSubmits: task.maxSubmits,
    attachments: latest?.attachments || [],
    reviewStatus,
    reviewerComment,
  }
}

export function quizForUser(quiz: QuizRecordSeed, userId?: number) {
  const records = quizRecords.filter((item) => item.quizId === quiz.id && item.userId === userId)
  return {
    ...quiz,
    attemptCount: records.length,
    bestScore: records.length ? Math.max(...records.map((item) => item.score)) : undefined,
  }
}
