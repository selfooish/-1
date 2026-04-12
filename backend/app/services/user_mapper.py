from __future__ import annotations

from app.data.mock_db import calc_level
from app.models.user import User


def orm_user_to_internal_dict(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "password_hash": user.password_hash,
        "avatar": user.avatar,
        "role": user.role,
        "points": user.points,
        "email": user.email,
        "phone": user.phone,
        "bio": user.bio,
        "createdAt": user.created_at.isoformat(),
    }


def orm_user_to_public_dict(user: User) -> dict:
    level, title = calc_level(user.points)
    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "role": user.role,
        "points": user.points,
        "level": level,
        "title": title,
        "createdAt": user.created_at.isoformat(),
        "email": user.email,
        "phone": user.phone,
        "bio": user.bio,
    }
