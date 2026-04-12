import bcrypt from 'bcryptjs'
import { Router } from 'express'
import { findUserByUsername, publicUser, users } from '../../data/mock-db.js'
import { signToken } from '../../shared/auth.js'
import { AppError, ok } from '../../shared/http.js'

export const authRouter = Router()

authRouter.post('/login', async (req, res, next) => {
  try {
    const { username, password } = req.body as { username?: string; password?: string }
    if (!username || !password) {
      throw new AppError('用户名和密码不能为空')
    }

    const user = findUserByUsername(username)
    if (!user) {
      throw new AppError('用户不存在', 401, 401)
    }

    const matched = await bcrypt.compare(password, user.passwordHash)
    if (!matched) {
      throw new AppError('用户名或密码错误', 401, 401)
    }

    const token = signToken({ userId: user.id, role: user.role })
    res.json(ok({ token, user: publicUser(user) }))
  } catch (error) {
    next(error)
  }
})

authRouter.post('/register', async (req, res, next) => {
  try {
    const { username, password, nickname } = req.body as {
      username?: string
      password?: string
      nickname?: string
    }

    if (!username || !password || !nickname) {
      throw new AppError('请完整填写注册信息')
    }

    if (findUserByUsername(username)) {
      throw new AppError('用户名已存在')
    }

    const passwordHash = await bcrypt.hash(password, 10)
    const created = {
      id: users.length + 1,
      username,
      nickname,
      passwordHash,
      avatar: '',
      role: 'student' as const,
      points: 0,
      createdAt: new Date().toISOString(),
    }

    users.push(created)

    const token = signToken({ userId: created.id, role: created.role })
    res.json(ok({ token, user: publicUser(created) }, '注册成功'))
  } catch (error) {
    next(error)
  }
})
