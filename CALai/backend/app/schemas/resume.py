"""
Resume schemas — upload, parsed data, SSE events.
"""

from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    id: str
    file_url: str
    file_type: str
    message: str = "Resume uploaded. Parsing started."


class ParsedResumeResponse(BaseModel):
    """Full parsed resume data returned to frontend."""
    id: str
    file_type: str
    skills: list[str] = []
    experience_years: float | None = None
    keywords: list[str] = []
    parsing_confidence: float | None = None
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
