"""
Application ORM model — tracks job applications per user.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Numeric,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Application(Base):
    __tablename__ = "applications"

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
    status: Mapped[str] = mapped_column(
        String(20), default="applied", nullable=False
    )
    match_score_at_apply: Mapped[float | None] = mapped_column(
        Numeric(5, 1), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(String(50), default="in_app")

    applied_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    status_updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="applications")
    job: Mapped["Job"] = relationship("Job", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="unique_user_job_app"),
        Index("idx_apps_user", "user_id", "applied_at"),
        Index("idx_apps_status", "user_id", "status"),
    )


from app.models.user import User  # noqa: E402
from app.models.job import Job  # noqa: E402
