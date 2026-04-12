import { Router } from 'express'
import { findUserById, publicUser } from '../../data/mock-db.js'
import { type AuthedRequest, requireAuth } from '../../shared/auth.js'
import { AppError, ok } from '../../shared/http.js'

export const userRouter = Router()

userRouter.get('/profile', requireAuth, (req: AuthedRequest, res, next) => {
  try {
    const user = findUserById(req.auth!.userId)
    if (!user) {
      throw new AppError('用户不存在', 404, 404)
    }
    res.json(ok(publicUser(user)))
  } catch (error) {
    next(error)
  }
})

userRouter.put('/profile', requireAuth, (req: AuthedRequest, res, next) => {
  try {
    const user = findUserById(req.auth!.userId)
    if (!user) {
      throw new AppError('用户不存在', 404, 404)
    }

    const { nickname, email, phone, bio, avatar } = req.body as {
      nickname?: string
      email?: string
      phone?: string
      bio?: string
      avatar?: string
    }

    user.nickname = nickname ?? user.nickname
    user.email = email ?? user.email
    user.phone = phone ?? user.phone
    user.bio = bio ?? user.bio
    user.avatar = avatar ?? user.avatar

    res.json(ok(publicUser(user), '更新成功'))
  } catch (error) {
    next(error)
  }
})
