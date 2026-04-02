import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior() {
    return { top: 0 }
  },
  routes: [
    // 首页
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/home/HomeView.vue'),
    },
    // 认证
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { guestOnly: true },
    },
    // 技能教程
    {
      path: '/tutorials',
      name: 'tutorials',
      component: () => import('@/views/tutorial/TutorialListView.vue'),
    },
    {
      path: '/tutorials/:id',
      name: 'tutorial-detail',
      component: () => import('@/views/tutorial/TutorialDetailView.vue'),
    },
    {
      path: '/tutorials/:id/learn/:chapterId?',
      name: 'tutorial-learn',
      component: () => import('@/views/tutorial/TutorialLearnView.vue'),
      meta: { requiresAuth: true },
    },
    // 题库与答题
    {
      path: '/quizzes',
      name: 'quizzes',
      component: () => import('@/views/quiz/QuizListView.vue'),
    },
    {
      path: '/quizzes/:id',
      name: 'quiz-detail',
      component: () => import('@/views/quiz/QuizDetailView.vue'),
    },
    {
      path: '/quizzes/:id/do',
      name: 'quiz-do',
      component: () => import('@/views/quiz/QuizDoView.vue'),
      meta: { requiresAuth: true },
    },
    // 实践任务
    {
      path: '/tasks',
      name: 'tasks',
      component: () => import('@/views/task/TaskListView.vue'),
    },
    {
      path: '/tasks/:id',
      name: 'task-detail',
      component: () => import('@/views/task/TaskDetailView.vue'),
    },
    {
      path: '/tasks/:id/submit',
      name: 'task-submit',
      component: () => import('@/views/task/TaskSubmitView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/my-tasks',
      name: 'my-tasks',
      component: () => import('@/views/task/MyTasksView.vue'),
      meta: { requiresAuth: true },
    },
    // 成长中心
    {
      path: '/growth',
      name: 'growth',
      component: () => import('@/views/growth/GrowthView.vue'),
      meta: { requiresAuth: true },
    },
    // 个人中心
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/profile/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    // CMS 后台
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/admin/AdminView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    // 404
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/error/NotFoundView.vue'),
    },
  ],
})

// 路由守卫
router.beforeEach((to) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.requiresAdmin && userStore.userInfo?.role !== 'admin') {
    return { name: 'home' }
  }

  if (to.meta.guestOnly && userStore.isLoggedIn) {
    return { name: 'home' }
  }
})

export default router
