"""
Job ORM model — matches implementation plan Component 2 spec.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Boolean,
    Numeric,
    DateTime,
    Date,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fingerprint: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    is_remote: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_clean: Mapped[str | None] = mapped_column(Text, nullable=True)
    job_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(20), nullable=True)

    salary_min: Mapped[int | None] = mapped_column(nullable=True)
    salary_max: Mapped[int | None] = mapped_column(nullable=True)
    salary_currency: Mapped[str | None] = mapped_column(String(3), nullable=True)

    skills_required: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, default=list
    )
    skills_preferred: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )

    responsibilities: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )

    source: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    posted_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Embedding stored as JSONB array for portability (pgvector optional)
    embedding: Mapped[list | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("idx_jobs_skills_required", "skills_required", postgresql_using="gin"),
        Index(
            "idx_jobs_active",
            "is_active",
            postgresql_where=is_active.is_(True),
        ),
    )
