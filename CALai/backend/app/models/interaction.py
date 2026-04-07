"""
UserInteraction + SavedJob ORM models — for recommendation engine signals.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id"),
        nullable=False,
    )
    action: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # view, click, save, unsave, dismiss, apply
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="interactions")
    job: Mapped["Job"] = relationship("Job", lazy="selectin")

    __table_args__ = (
        Index("idx_interactions_user", "user_id", "created_at"),
        Index("idx_interactions_action", "action", "created_at"),
    )


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id"),
        nullable=False,
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    job: Mapped["Job"] = relationship("Job", lazy="selectin")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "job_id"),
    )


from app.models.user import User  # noqa: E402
from app.models.job import Job  # noqa: E402
