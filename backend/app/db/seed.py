from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.growth import Badge
from app.models.user import User


def seed_users(db: Session) -> None:
    users = [
        {
            "id": 1,
            "username": "student",
            "nickname": "小明",
            "password_hash": hash_password("123456"),
            "avatar": "",
            "role": "student",
            "points": 850,
            "email": "xiaoming@example.com",
            "phone": "13800000000",
            "bio": "热爱劳动，喜欢动手实践，正在学习更多生活技能。",
        },
        {
            "id": 2,
            "username": "admin",
            "nickname": "管理员",
            "password_hash": hash_password("123456"),
            "avatar": "",
            "role": "admin",
            "points": 1800,
            "email": "",
            "phone": "",
            "bio": "",
        },
    ]

    for item in users:
        exists = db.query(User).filter(User.username == item["username"]).first()
        if exists:
            continue
        db.add(User(**item))


def seed_badges(db: Session) -> None:
    badges = [
        {
            "name": "初学者",
            "description": "完成第一个教程",
            "icon": "🌱",
            "color": "#42b883",
            "badge_type": "skill",
            "requirement": "完成 1 个教程",
        },
        {
            "name": "答题达人",
            "description": "完成 10 次答题",
            "icon": "📝",
            "color": "#3498db",
            "badge_type": "quiz",
            "requirement": "完成 10 次答题",
        },
    ]

    for item in badges:
        exists = db.query(Badge).filter(Badge.name == item["name"]).first()
        if exists:
            continue
        db.add(Badge(**item))


def run_seed() -> None:
    db = SessionLocal()
    try:
        seed_users(db)
        seed_badges(db)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
