"""
Job ORM model — aligned with Supabase public.jobs schema.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Boolean,
    Integer,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    external_id: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    job_type: Mapped[str | None] = mapped_column(
        String(30), default="full-time", nullable=True
    )
    experience_level: Mapped[str | None] = mapped_column(
        String(20), default="mid", nullable=True
    )

    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str | None] = mapped_column(
        String(3), default="USD", nullable=True
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsibilities: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )
    requirements: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )
    required_skills: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), default=list, nullable=True
    )
    preferred_skills: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), default=list, nullable=True
    )
    benefits: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )

    application_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Embedding stored as pgvector vector(384) in Supabase
    # Access it via raw SQL when needed for similarity queries
    # embedding column exists but we don't map it directly to avoid pgvector dependency

    is_active: Mapped[bool | None] = mapped_column(
        Boolean, default=True, nullable=True
    )
    is_remote: Mapped[bool | None] = mapped_column(
        Boolean, default=False, nullable=True
    )

    posted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
