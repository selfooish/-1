export interface User {
  id: number
  username: string
  nickname: string
  avatar: string
  role: 'student' | 'teacher' | 'admin'
  points: number
  level: number
  title: string
  createdAt: string
  email?: string
  phone?: string
  bio?: string
}

export interface LoginForm {
  username: string
  password: string
}

export interface RegisterForm {
  username: string
  password: string
  nickname: string
}

export type TutorialCategory = string

export interface Chapter {
  id: number
  title: string
  duration: string
  isFree: boolean
  isCompleted: boolean
  videoUrl?: string
}

export interface Tutorial {
  id: number
  title: string
  category: TutorialCategory
  coverImage: string
  description: string
  duration: string
  difficulty: 'easy' | 'medium' | 'hard'
  author: string
  authorAvatar: string
  viewCount: number
  collectCount: number
  isCollected: boolean
  isPurchased: boolean
  tags: string[]
  chapters: Chapter[]
  rating: number
  reviewCount: number
  createdAt: string
  updatedAt: string
}

export interface TutorialListItem {
  id: number
  title: string
  category: TutorialCategory
  coverImage: string
  description: string
  duration: string
  difficulty: 'easy' | 'medium' | 'hard'
  author: string
  viewCount: number
  collectCount: number
  rating: number
  reviewCount: number
  isCollected?: boolean
}

export interface QuestionOption {
  label: string
  text: string
}

export interface Question {
  id: number
  type: 'single' | 'multiple' | 'judge' | 'essay'
  stem: string
  options?: QuestionOption[]
  answer: string | string[]
  explanation: string
  difficulty: 'easy' | 'medium' | 'hard'
  category: string
  tags: string[]
}

export interface Quiz {
  id: number
  title: string
  description: string
  questionCount: number
  timeLimit: number
  passScore: number
  totalScore: number
  attemptCount: number
  bestScore?: number
  category: TutorialCategory | string
  difficulty: 'easy' | 'medium' | 'hard'
  tags: string[]
  createdAt: string
}

export interface UserAnswer {
  questionId: number
  userAnswer: string | string[]
  isCorrect: boolean
  score: number
}

export interface QuizRecord {
  id: number
  quizId: number
  quizTitle: string
  score: number
  totalScore: number
  correctCount: number
  totalQuestions: number
  timeSpent: number
  submittedAt: string
  answers: UserAnswer[]
}

export interface Attachment {
  name: string
  url: string
  type: 'image' | 'video' | 'document' | string
  size: number
}

export interface Task {
  id: number
  title: string
  description: string
  category: TutorialCategory
  coverImage: string
  points: number
  difficulty: 'easy' | 'medium' | 'hard'
  deadline: string
  status: 'pending' | 'in_progress' | 'submitted' | 'reviewed'
  submitCount: number
  maxSubmits: number
  attachments: Attachment[]
  reviewStatus?: 'excellent' | 'pass' | 'fail'
  reviewerComment?: string
  createdAt: string
}

export interface TaskSubmission {
  id: number
  taskId: number
  content: string
  attachments: Attachment[]
  submittedAt: string
  status: 'pending' | 'approved' | 'rejected'
  points?: number
  reviewerComment?: string
}

export interface PointRecord {
  id: number
  type: 'tutorial' | 'quiz' | 'task' | 'review' | 'daily' | 'other'
  action: string
  points: number
  createdAt: string
  relatedId?: number
  relatedTitle?: string
}

export interface Badge {
  id: number
  name: string
  description: string
  icon: string
  color: string
  type: 'skill' | 'task' | 'quiz' | 'streak' | 'special'
  requirement: string
  unlockedAt?: string | null
  progress?: number
  total?: number
}

export interface GrowthData {
  date: string
  points: number
  tasksCompleted: number
  tutorialsCompleted: number
  quizzesTaken: number
}

export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}
