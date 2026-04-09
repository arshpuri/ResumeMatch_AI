"""
Resume schemas — upload, parsed data, SSE events.
Aligned with Supabase schema column names.
"""

from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    id: str
    file_key: str
    file_name: str
    message: str = "Resume uploaded. Parsing started."


class ParsedResumeResponse(BaseModel):
    """Full parsed resume data returned to frontend."""
    id: str
    file_name: str | None = None
    mime_type: str | None = None
    skills: list[str] = []
    experience_years: float | None = None
    keywords: list[str] = []
    confidence_score: float | None = None
    parsing_status: str | None = None
    parsed_data: dict = {}

    model_config = {"from_attributes": True}


class ResumeUpdateRequest(BaseModel):
    """Manual edits to parsed resume fields."""
    skills: list[str] | None = None
    parsed_data: dict | None = None


class ParsingProgressEvent(BaseModel):
    """SSE event sent during resume parsing."""
    step: str  # extracting, sections, parsing, normalizing, matching
    progress: int  # 0 - 100
    status: str  # waiting, in_progress, done, error
    message: str | None = None
