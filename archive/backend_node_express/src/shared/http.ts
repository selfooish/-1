export interface ApiSuccess<T> {
  code: number
  message: string
  data: T
}

export function ok<T>(data: T, message = 'ok'): ApiSuccess<T> {
  return {
    code: 0,
    message,
    data,
  }
}

export class AppError extends Error {
  statusCode: number
  code: number

  constructor(message: string, statusCode = 400, code = statusCode) {
    super(message)
    this.statusCode = statusCode
    this.code = code
  }
}
