from typing import Literal

from pydantic import BaseModel, Field


class AttachmentOut(BaseModel):
    name: str
    url: str
    type: Literal["image", "video", "document"]
    size: int


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    coverImage: str
    points: int
    difficulty: Literal["easy", "medium", "hard"]
    deadline: str
    status: Literal["pending", "in_progress", "submitted", "reviewed"]
    submitCount: int
    maxSubmits: int
    attachments: list[AttachmentOut]
    reviewStatus: Literal["excellent", "pass", "fail"] | None = None
    reviewerComment: str | None = None
    createdAt: str


class TaskSubmissionCreate(BaseModel):
    content: str = Field(min_length=1)
    attachments: list[AttachmentOut] = []


class TaskSubmissionOut(BaseModel):
    id: int
    taskId: int
    content: str
    attachments: list[AttachmentOut]
    submittedAt: str
    status: Literal["pending", "approved", "rejected"]
    points: int | None = None
    reviewerComment: str | None = None

