from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models import (  # noqa: E402,F401
    Badge,
    PointRecord,
    Quiz,
    QuizAnswer,
    QuizOption,
    QuizQuestion,
    QuizRecord,
    Task,
    TaskSubmission,
    TaskSubmissionAttachment,
    Tutorial,
    TutorialChapter,
    TutorialChapterProgress,
    TutorialCollection,
    User,
    UserBadge,
)
