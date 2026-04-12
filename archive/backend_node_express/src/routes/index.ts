import { Router } from 'express'
import { ok } from '../shared/http.js'
import { adminRouter } from '../modules/admin/admin.routes.js'
import { authRouter } from '../modules/auth/auth.routes.js'
import { growthRouter } from '../modules/growth/growth.routes.js'
import { quizRecordRouter, quizRouter } from '../modules/quiz/quiz.routes.js'
import { taskRouter } from '../modules/task/task.routes.js'
import { tutorialRouter } from '../modules/tutorial/tutorial.routes.js'
import { userRouter } from '../modules/user/user.routes.js'

export const apiRouter = Router()

apiRouter.get('/health', (_req, res) => {
  res.json(ok({ status: 'ok' }))
})

apiRouter.use('/auth', authRouter)
apiRouter.use('/user', userRouter)
apiRouter.use('/tutorials', tutorialRouter)
apiRouter.use('/tasks', taskRouter)
apiRouter.use('/quizzes', quizRouter)
apiRouter.use('/quiz-records', quizRecordRouter)
apiRouter.use('/', growthRouter)
apiRouter.use('/admin', adminRouter)
