from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="student", nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    email: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    phone: Mapped[str] = mapped_column(String(50), default="", nullable=False)
    bio: Mapped[str] = mapped_column(Text, default="", nullable=False)

    tutorial_collections = relationship("TutorialCollection", back_populates="user", cascade="all, delete-orphan")
    chapter_progresses = relationship(
        "TutorialChapterProgress", back_populates="user", cascade="all, delete-orphan"
    )
    task_submissions = relationship("TaskSubmission", back_populates="user", cascade="all, delete-orphan")
    quiz_records = relationship("QuizRecord", back_populates="user", cascade="all, delete-orphan")
    point_records = relationship("PointRecord", back_populates="user", cascade="all, delete-orphan")
    user_badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
