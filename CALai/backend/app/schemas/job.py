"""
Job schemas — matches frontend JobMatch interface exactly.

Frontend expects:
{
  id, title, company, location, matchScore, salary?,
  postedAt, skills: string[], missingSkills: string[],
  reasons: string[]
}
"""

from pydantic import BaseModel


class JobMatchResponse(BaseModel):
    """Matches frontend JobMatch interface exactly."""
    id: str
    title: str
    company: str
    location: str
    matchScore: int
    salary: str | None = None
    postedAt: str
    skills: list[str] = []
    missingSkills: list[str] = []
    reasons: list[str] = []


class JobDetailResponse(BaseModel):
    """Extended job detail for /jobs/[id] page."""
    id: str
    title: str
    company: str
    location: str
    matchScore: int
    salary: str | None = None
    postedAt: str
    skills: list[str] = []
    missingSkills: list[str] = []
    reasons: list[str] = []
    description: str | None = None
    responsibilities: list[str] = []
    experienceLevel: str | None = None
    jobType: str | None = None
    isRemote: bool = False
    isSaved: bool = False


class JobFeedResponse(BaseModel):
    """Paginated job feed response."""
    jobs: list[JobMatchResponse]
    nextCursor: str | None = None
    total: int = 0


class JobSearchResponse(BaseModel):
    jobs: list[JobMatchResponse]
    total: int = 0
    query: str = ""


class JobActionResponse(BaseModel):
    success: bool = True
    message: str = ""
