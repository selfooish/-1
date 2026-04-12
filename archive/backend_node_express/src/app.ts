import cors from 'cors'
import express from 'express'
import { apiRouter } from './routes/index.js'
import { errorHandler } from './shared/error-handler.js'
import { env } from './shared/env.js'

export const app = express()

app.use(
  cors({
    origin: env.CLIENT_ORIGIN,
    credentials: true,
  })
)
app.use(express.json({ limit: '2mb' }))
app.use(express.urlencoded({ extended: true }))

app.use('/api', apiRouter)
app.use(errorHandler)
