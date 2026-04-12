from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Task(TimestampMixin, Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    cover_image: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    deadline_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    max_submits: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    submissions = relationship("TaskSubmission", back_populates="task", cascade="all, delete-orphan")


class TaskSubmission(TimestampMixin, Base):
    __tablename__ = "task_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="", nullable=False)
    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    points_awarded: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reviewer_comment: Mapped[str] = mapped_column(Text, default="", nullable=False)

    task = relationship("Task", back_populates="submissions")
    user = relationship("User", back_populates="task_submissions")
    attachments = relationship(
        "TaskSubmissionAttachment", back_populates="submission", cascade="all, delete-orphan"
    )


class TaskSubmissionAttachment(Base):
    __tablename__ = "task_submission_attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("task_submissions.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), default="image", nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    submission = relationship("TaskSubmission", back_populates="attachments")
