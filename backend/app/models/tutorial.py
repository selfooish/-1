from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Tutorial(TimestampMixin, Base):
    __tablename__ = "tutorials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    cover_image: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    duration_text: Mapped[str] = mapped_column(String(50), default="", nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    author_avatar: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    collect_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    review_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    chapters = relationship("TutorialChapter", back_populates="tutorial", cascade="all, delete-orphan")
    collections = relationship("TutorialCollection", back_populates="tutorial", cascade="all, delete-orphan")


class TutorialChapter(TimestampMixin, Base):
    __tablename__ = "tutorial_chapters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tutorial_id: Mapped[int] = mapped_column(ForeignKey("tutorials.id", ondelete="CASCADE"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    duration_text: Mapped[str] = mapped_column(String(50), default="", nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_free: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    video_url: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    video_storage_key: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    cover_image: Mapped[str] = mapped_column(String(500), default="", nullable=False)

    tutorial = relationship("Tutorial", back_populates="chapters")
    progresses = relationship("TutorialChapterProgress", back_populates="chapter", cascade="all, delete-orphan")


class TutorialCollection(Base):
    __tablename__ = "tutorial_collections"
    __table_args__ = (UniqueConstraint("user_id", "tutorial_id", name="uq_tutorial_collection"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tutorial_id: Mapped[int] = mapped_column(ForeignKey("tutorials.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="tutorial_collections")
    tutorial = relationship("Tutorial", back_populates="collections")


class TutorialChapterProgress(Base):
    __tablename__ = "tutorial_chapter_progress"
    __table_args__ = (UniqueConstraint("user_id", "chapter_id", name="uq_tutorial_chapter_progress"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("tutorial_chapters.id", ondelete="CASCADE"), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="chapter_progresses")
    chapter = relationship("TutorialChapter", back_populates="progresses")
