from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)


def create_user(
    db: Session,
    *,
    username: str,
    nickname: str,
    password_hash: str,
    role: str = "student",
) -> User:
    user = User(
        username=username,
        nickname=nickname,
        password_hash=password_hash,
        avatar="",
        role=role,
        points=0,
        email="",
        phone="",
        bio="",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_profile(db: Session, user: User, **payload) -> User:
    for key, value in payload.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
