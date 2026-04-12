# Backend Scaffold

## Quick Start

```bash
cd backend
npm install
npm run dev
```

Server defaults:

- API base: `http://localhost:3000/api`
- Health check: `GET /api/health`

## What This Scaffold Includes

- Express + TypeScript backend skeleton
- Unified response format: `{ code, message, data }`
- JWT auth middleware
- In-memory mock data for rapid frontend integration
- Modules aligned with the frontend project:
  - auth
  - user
  - tutorials
  - tasks
  - quizzes
  - growth
  - admin

## Important Notes

- All data is currently stored in memory in `src/data/mock-db.ts`
- Restarting the server resets data
- Replace the mock data layer with a real database next
- This scaffold is intentionally shaped to match the existing frontend stores

## Suggested Next Steps

1. Replace `mock-db.ts` with Prisma / MySQL or your preferred persistence layer
2. Move auth, tutorial, task, quiz logic into services
3. Add validation and Swagger
4. Add upload support for task attachments
