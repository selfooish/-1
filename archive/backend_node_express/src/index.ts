import { app } from './app.js'
import { env } from './shared/env.js'

app.listen(env.PORT, () => {
  console.log(`API server running on http://localhost:${env.PORT}/api`)
})
