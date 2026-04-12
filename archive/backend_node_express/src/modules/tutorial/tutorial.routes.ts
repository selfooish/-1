import { Router } from 'express'
import { collections, completedChapters, tutorials, tutorialForUser, tutorialListItemForUser } from '../../data/mock-db.js'
import { type AuthedRequest, requireAuth } from '../../shared/auth.js'
import { AppError, ok } from '../../shared/http.js'

export const tutorialRouter = Router()

tutorialRouter.get('/', (req, res) => {
  const { category, difficulty, keyword = '', page = '1', pageSize = '20' } = req.query
  const currentPage = Number(page)
  const currentPageSize = Number(pageSize)

  const list = tutorials
    .filter((item) => !category || item.category === category)
    .filter((item) => !difficulty || item.difficulty === difficulty)
    .filter((item) => item.title.includes(String(keyword)))

  const sliced = list.slice((currentPage - 1) * currentPageSize, currentPage * currentPageSize)

  res.json(
    ok({
      list: sliced.map((item) => tutorialListItemForUser(item)),
      total: list.length,
      page: currentPage,
      pageSize: currentPageSize,
    })
  )
})

tutorialRouter.get('/:id', (req, res, next) => {
  try {
    const id = Number(req.params.id)
    const tutorial = tutorials.find((item) => item.id === id)
    if (!tutorial) {
      throw new AppError('教程不存在', 404, 404)
    }

    res.json(ok(tutorialForUser(tutorial)))
  } catch (error) {
    next(error)
  }
})

tutorialRouter.post('/:id/collect', requireAuth, (req: AuthedRequest, res) => {
  collections.add(`${req.auth!.userId}:${Number(req.params.id)}`)
  res.json(ok(true, '收藏成功'))
})

tutorialRouter.delete('/:id/collect', requireAuth, (req: AuthedRequest, res) => {
  collections.delete(`${req.auth!.userId}:${Number(req.params.id)}`)
  res.json(ok(true, '取消收藏成功'))
})

tutorialRouter.post('/:tutorialId/chapters/:chapterId/complete', requireAuth, (req: AuthedRequest, res) => {
  completedChapters.add(`${req.auth!.userId}:${Number(req.params.chapterId)}`)
  res.json(ok(true, '章节完成已记录'))
})
