"""init tables

Revision ID: 20260412_000001
Revises: None
Create Date: 2026-04-12 00:00:01
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260412_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "badges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("icon", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("color", sa.String(length=20), nullable=False, server_default="#42b883"),
        sa.Column("badge_type", sa.String(length=20), nullable=False),
        sa.Column("requirement", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "quizzes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("question_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("time_limit_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("pass_score", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("total_score", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_quizzes_id", "quizzes", ["id"])
    op.create_index("ix_quizzes_category", "quizzes", ["category"])
    op.create_index("ix_quizzes_difficulty", "quizzes", ["difficulty"])

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("cover_image", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("deadline_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("max_submits", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_tasks_id", "tasks", ["id"])
    op.create_index("ix_tasks_category", "tasks", ["category"])
    op.create_index("ix_tasks_difficulty", "tasks", ["difficulty"])

    op.create_table(
        "tutorials",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("cover_image", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("duration_text", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("author_name", sa.String(length=100), nullable=False),
        sa.Column("author_avatar", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("collect_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rating", sa.Float(), nullable=False, server_default="0"),
        sa.Column("review_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_tutorials_id", "tutorials", ["id"])
    op.create_index("ix_tutorials_category", "tutorials", ["category"])
    op.create_index("ix_tutorials_difficulty", "tutorials", ["difficulty"])

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("nickname", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("avatar", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("role", sa.String(length=20), nullable=False, server_default="student"),
        sa.Column("points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("email", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("phone", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("bio", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_username", "users", ["username"])

    op.create_table(
        "point_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("record_type", sa.String(length=20), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("related_id", sa.Integer(), nullable=True),
        sa.Column("related_title", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_point_records_id", "point_records", ["id"])
    op.create_index("ix_point_records_record_type", "point_records", ["record_type"])

    op.create_table(
        "quiz_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("quiz_id", sa.Integer(), sa.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("question_type", sa.String(length=20), nullable=False),
        sa.Column("stem", sa.Text(), nullable=False),
        sa.Column("correct_answer", sa.JSON(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False, server_default=""),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_quiz_questions_id", "quiz_questions", ["id"])

    op.create_table(
        "quiz_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("quiz_id", sa.Integer(), sa.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_score", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("correct_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_questions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("time_spent_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_quiz_records_id", "quiz_records", ["id"])

    op.create_table(
        "quiz_options",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("label", sa.String(length=10), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
    )
    op.create_index("ix_quiz_options_id", "quiz_options", ["id"])

    op.create_table(
        "quiz_answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("record_id", sa.Integer(), sa.ForeignKey("quiz_records.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_answer", sa.JSON(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("score_awarded", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_quiz_answers_id", "quiz_answers", ["id"])

    op.create_table(
        "task_submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("points_awarded", sa.Integer(), nullable=True),
        sa.Column("reviewer_comment", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_task_submissions_id", "task_submissions", ["id"])

    op.create_table(
        "task_submission_attachments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("submission_id", sa.Integer(), sa.ForeignKey("task_submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("file_type", sa.String(length=50), nullable=False, server_default="image"),
        sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_task_submission_attachments_id", "task_submission_attachments", ["id"])

    op.create_table(
        "tutorial_chapters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tutorial_id", sa.Integer(), sa.ForeignKey("tutorials.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("duration_text", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("duration_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_free", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("video_url", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("video_storage_key", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("cover_image", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_tutorial_chapters_id", "tutorial_chapters", ["id"])

    op.create_table(
        "tutorial_chapter_progress",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chapter_id", sa.Integer(), sa.ForeignKey("tutorial_chapters.id", ondelete="CASCADE"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "chapter_id", name="uq_tutorial_chapter_progress"),
    )

    op.create_table(
        "tutorial_collections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tutorial_id", sa.Integer(), sa.ForeignKey("tutorials.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("user_id", "tutorial_id", name="uq_tutorial_collection"),
    )

    op.create_table(
        "user_badges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("badge_id", sa.Integer(), sa.ForeignKey("badges.id", ondelete="CASCADE"), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),
    )


def downgrade() -> None:
    op.drop_table("user_badges")
    op.drop_table("tutorial_collections")
    op.drop_table("tutorial_chapter_progress")
    op.drop_index("ix_tutorial_chapters_id", table_name="tutorial_chapters")
    op.drop_table("tutorial_chapters")
    op.drop_index("ix_task_submission_attachments_id", table_name="task_submission_attachments")
    op.drop_table("task_submission_attachments")
    op.drop_index("ix_task_submissions_id", table_name="task_submissions")
    op.drop_table("task_submissions")
    op.drop_index("ix_quiz_answers_id", table_name="quiz_answers")
    op.drop_table("quiz_answers")
    op.drop_index("ix_quiz_options_id", table_name="quiz_options")
    op.drop_table("quiz_options")
    op.drop_index("ix_quiz_records_id", table_name="quiz_records")
    op.drop_table("quiz_records")
    op.drop_index("ix_quiz_questions_id", table_name="quiz_questions")
    op.drop_table("quiz_questions")
    op.drop_index("ix_point_records_record_type", table_name="point_records")
    op.drop_index("ix_point_records_id", table_name="point_records")
    op.drop_table("point_records")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_tutorials_difficulty", table_name="tutorials")
    op.drop_index("ix_tutorials_category", table_name="tutorials")
    op.drop_index("ix_tutorials_id", table_name="tutorials")
    op.drop_table("tutorials")
    op.drop_index("ix_tasks_difficulty", table_name="tasks")
    op.drop_index("ix_tasks_category", table_name="tasks")
    op.drop_index("ix_tasks_id", table_name="tasks")
    op.drop_table("tasks")
    op.drop_index("ix_quizzes_difficulty", table_name="quizzes")
    op.drop_index("ix_quizzes_category", table_name="quizzes")
    op.drop_index("ix_quizzes_id", table_name="quizzes")
    op.drop_table("quizzes")
    op.drop_table("badges")
