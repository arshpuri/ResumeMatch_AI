"""
ParsedResume ORM model — matches 02_resume_parsing_engine.md schema.
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
    file_url: Mapped[str] = mapped_column(Text, nullable=False)
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    skills: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, default=list
    )
    experience_years: Mapped[float | None] = mapped_column(
        Numeric(4, 1), nullable=True
    )
    keywords: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )
    parsing_confidence: Mapped[float | None] = mapped_column(
        Numeric(3, 2), nullable=True
    )
    parser_version: Mapped[str | None] = mapped_column(String(20), nullable=True)

    parsed_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="resume")

    __table_args__ = (
        UniqueConstraint("user_id", name="unique_user_resume"),
        Index("idx_resume_skills", "skills", postgresql_using="gin"),
        Index("idx_resume_keywords", "keywords", postgresql_using="gin"),
    )


from app.models.user import User  # noqa: E402
