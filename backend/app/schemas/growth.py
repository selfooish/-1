from typing import Literal

from pydantic import BaseModel


class PointRecordOut(BaseModel):
    id: int
    type: Literal["tutorial", "quiz", "task", "review", "daily", "other"]
    action: str
    points: int
    createdAt: str
    relatedId: int | None = None
    relatedTitle: str | None = None


class BadgeOut(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    color: str
    type: Literal["skill", "task", "quiz", "streak", "special"]
    requirement: str
    unlockedAt: str | None = None
    progress: int | None = None
    total: int | None = None


class GrowthDataOut(BaseModel):
    date: str
    points: int
    tasksCompleted: int
    tutorialsCompleted: int
    quizzesTaken: int

