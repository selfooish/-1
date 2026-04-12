import { Router } from 'express'
import { taskForUser, tasks, taskSubmissions } from '../../data/mock-db.js'
import { type AuthedRequest, requireAuth } from '../../shared/auth.js'
import { AppError, ok } from '../../shared/http.js'

export const taskRouter = Router()

taskRouter.get('/', (req, res) => {
  const { category, page = '1' } = req.query
  const currentPage = Number(page)
  const pageSize = 20

  const list = tasks.filter((item) => !category || item.category === category)
  const sliced = list.slice((currentPage - 1) * pageSize, currentPage * pageSize)

  res.json(
    ok({
      list: sliced.map((item) => taskForUser(item)),
      total: list.length,
      page: currentPage,
      pageSize,
    })
  )
})

taskRouter.get('/my', requireAuth, (req: AuthedRequest, res) => {
  res.json(ok(tasks.map((task) => taskForUser(task, req.auth!.userId))))
})

taskRouter.get('/:id', (req, res, next) => {
  try {
    const task = tasks.find((item) => item.id === Number(req.params.id))
    if (!task) {
      throw new AppError('任务不存在', 404, 404)
    }
    res.json(ok(taskForUser(task)))
  } catch (error) {
    next(error)
  }
})

taskRouter.post('/:taskId/submit', requireAuth, (req: AuthedRequest, res, next) => {
  try {
    const taskId = Number(req.params.taskId)
    const task = tasks.find((item) => item.id === taskId)
    if (!task) {
      throw new AppError('任务不存在', 404, 404)
    }

    const { content, attachments = [] } = req.body as {
      content?: string
      attachments?: Array<{ name: string; url: string; type: 'image' | 'video' | 'document'; size?: number }>
    }

    if (!content?.trim()) {
      throw new AppError('提交内容不能为空')
    }

    const record = {
      id: taskSubmissions.length + 1,
      taskId,
      userId: req.auth!.userId,
      content,
      attachments: attachments.map((item) => ({
        ...item,
        size: item.size ?? 0,
      })),
      submittedAt: new Date().toISOString(),
      status: 'pending' as const,
      reviewerComment: '',
    }

    taskSubmissions.unshift(record)
    res.json(ok(record, '提交成功'))
  } catch (error) {
    next(error)
  }
})
