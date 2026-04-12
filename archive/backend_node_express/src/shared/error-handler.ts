import type { NextFunction, Request, Response } from 'express'
import { AppError } from './http.js'

export function errorHandler(
  error: Error,
  _req: Request,
  res: Response,
  _next: NextFunction
) {
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      code: error.code,
      message: error.message,
      data: null,
    })
  }

  console.error(error)
  return res.status(500).json({
    code: 500,
    message: '服务器内部错误',
    data: null,
  })
}
