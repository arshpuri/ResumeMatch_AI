"""
User ORM model — aligned with Supabase public.users schema.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Text,
    Index,
    ForeignKey,
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
    auth_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False, default=""
    )
    headline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    portfolio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(
        String(50), default="Open to Work", nullable=True
    )
    preferences: Mapped[dict | None] = mapped_column(
        JSONB, default=dict, nullable=True
    )
    is_active: Mapped[bool | None] = mapped_column(
        Boolean, default=True, nullable=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
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


# Avoid circular imports — these are resolved at runtime by SQLAlchemy
from app.models.resume import ParsedResume  # noqa: E402
from app.models.application import Application  # noqa: E402
from app.models.interaction import UserInteraction  # noqa: E402
