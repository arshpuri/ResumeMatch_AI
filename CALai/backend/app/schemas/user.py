"""
User / Profile schemas — matches frontend USER_PROFILE shape exactly.

Frontend expects:
{
  name, headline, location, status, completionScore,
  skills: string[],
  experience: [{ id, role, company, period, bullets: string[] }],
  education: [{ id, degree, institution, period }]
}
"""

from pydantic import BaseModel, Field


class ExperienceItem(BaseModel):
    id: str
    role: str
    company: str
    period: str
    bullets: list[str] = []


class EducationItem(BaseModel):
    id: str
    degree: str
    institution: str
    period: str


class UserProfileResponse(BaseModel):
    """Matches frontend USER_PROFILE mock data shape."""
    name: str
    headline: str | None = ""
    location: str | None = ""
    status: str = "Open to Work"
    completionScore: int = 0
    skills: list[str] = []
    experience: list[ExperienceItem] = []
    education: list[EducationItem] = []

    model_config = {"from_attributes": True}


class ProfileUpdateRequest(BaseModel):
    name: str | None = None
    headline: str | None = None
    location: str | None = None
    status: str | None = None
    phone: str | None = None


class SkillsUpdateRequest(BaseModel):
    skills: list[str]


class SkillGap(BaseModel):
    skill: str
    frequency: int
    percentage: float


class SkillGapResponse(BaseModel):
    gaps: list[SkillGap]
    total_jobs_analyzed: int
