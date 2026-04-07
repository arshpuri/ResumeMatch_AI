"""
User ORM model — matches 06_backend_and_database.md schema exactly.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Text,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    headline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    auth_provider: Mapped[str] = mapped_column(
        String(20), default="email", nullable=False
    )
    auth_provider_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    preferences: Mapped[dict] = mapped_column(JSONB, default=dict)
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(50), default="Open to Work")

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    resume: Mapped["ParsedResume"] = relationship(
        "ParsedResume", back_populates="user", uselist=False, lazy="selectin"
    )
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="user", lazy="selectin"
    )
    interactions: Mapped[list["UserInteraction"]] = relationship(
        "UserInteraction", back_populates="user", lazy="noload"
    )

    __table_args__ = (
        Index("idx_users_provider", "auth_provider", "auth_provider_id"),
    )


# Avoid circular imports — these are resolved at runtime by SQLAlchemy
from app.models.resume import ParsedResume  # noqa: E402
from app.models.application import Application  # noqa: E402
from app.models.interaction import UserInteraction  # noqa: E402
