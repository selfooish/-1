from typing import Literal

from pydantic import BaseModel


class ChapterOut(BaseModel):
    id: int
    title: str
    duration: str
    isFree: bool
    isCompleted: bool
    videoUrl: str | None = None


class TutorialListItemOut(BaseModel):
    id: int
    title: str
    category: str
    coverImage: str
    description: str
    duration: str
    difficulty: Literal["easy", "medium", "hard"]
    author: str
    viewCount: int
    collectCount: int
    rating: float
    reviewCount: int
    isCollected: bool = False


class TutorialOut(TutorialListItemOut):
    authorAvatar: str
    isPurchased: bool
    tags: list[str]
    chapters: list[ChapterOut]
    createdAt: str
    updatedAt: str

