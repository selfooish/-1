import jwt from 'jsonwebtoken'
import type { NextFunction, Request, Response } from 'express'
import { findUserById } from '../data/mock-db.js'
import { env } from './env.js'
import { AppError } from './http.js'

export type UserRole = 'student' | 'teacher' | 'admin'

export interface AuthPayload {
  userId: number
  role: UserRole
}

export interface AuthedRequest extends Request {
  auth?: AuthPayload
}

export function signToken(payload: AuthPayload) {
  return jwt.sign(payload, env.JWT_SECRET, { expiresIn: '7d' })
}

export function requireAuth(req: AuthedRequest, _res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization
  if (!authHeader?.startsWith('Bearer ')) {
    return next(new AppError('未登录', 401, 401))
  }

  const token = authHeader.slice(7)

  try {
    const payload = jwt.verify(token, env.JWT_SECRET) as AuthPayload
    const user = findUserById(payload.userId)
    if (!user) {
      return next(new AppError('用户不存在', 401, 401))
    }
    req.auth = payload
    return next()
  } catch {
    return next(new AppError('登录状态失效', 401, 401))
  }
}

export function requireAdmin(req: AuthedRequest, _res: Response, next: NextFunction) {
  if (!req.auth) {
    return next(new AppError('未登录', 401, 401))
  }
  if (req.auth.role !== 'admin') {
    return next(new AppError('无权限访问', 403, 403))
  }
  return next()
}
