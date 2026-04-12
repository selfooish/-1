from typing import Literal

from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    avatar: str
    role: Literal["student", "teacher", "admin"]
    points: int
    level: int
    title: str
    createdAt: str
    email: str = ""
    phone: str = ""
    bio: str = ""


class UserProfileUpdate(BaseModel):
    nickname: str | None = None
    avatar: str | None = None
    email: str | None = None
    phone: str | None = None
    bio: str | None = None

