"""
ParsedResume ORM model — aligned with Supabase public.parsed_resumes schema.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ParsedResume(Base):
    __tablename__ = "parsed_resumes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_data: Mapped[dict | None] = mapped_column(
        JSONB, default=dict, nullable=True
    )
    skills: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), default=list, nullable=True
    )
    keywords: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), default=list, nullable=True
    )
    experience_years: Mapped[float | None] = mapped_column(
        Float, default=0, nullable=True
    )
    education_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(
        Float, default=0, nullable=True
    )
    parsing_status: Mapped[str | None] = mapped_column(
        String(20), default="pending", nullable=True
    )
    parsing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int | None] = mapped_column(Integer, default=1, nullable=True)
    is_primary: Mapped[bool | None] = mapped_column(
        Boolean, default=True, nullable=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="resume")


from app.models.user import User  # noqa: E402
