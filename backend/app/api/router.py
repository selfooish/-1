from fastapi import APIRouter

from app.api.routes import admin, auth, growth, quizzes, tasks, tutorials, users
from app.schemas.common import success_response


api_router = APIRouter()


@api_router.get("/health")
def health():
    return success_response({"status": "ok"})


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/user", tags=["user"])
api_router.include_router(tutorials.router, prefix="/tutorials", tags=["tutorials"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(quizzes.record_router, prefix="/quiz-records", tags=["quiz-records"])
api_router.include_router(growth.router, tags=["growth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

