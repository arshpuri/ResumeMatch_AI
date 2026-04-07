"""
Final ranking — weighted combination of 3 layers from 04_recommendation_engine.md.

Final Score = 0.35 × keyword_score + 0.45 × semantic_score + 0.20 × personalization_score
"""

from datetime import datetime, timezone

from app.matching.keyword_matcher import (
    keyword_match_score,
    get_matching_skills,
    get_missing_skills,
)
from app.matching.semantic_matcher import semantic_similarity
from app.matching.personalizer import personalization_score
from app.parsing.skill_normalizer import normalize_skills, get_display_name

# Weights from blueprint (tuned via A/B testing)
WEIGHTS = {
    "keyword": 0.35,
    "semantic": 0.45,
    "personalization": 0.20,
}


def compute_match_score(
    resume_skills: list[str],
    resume_exp_years: float,
    resume_embedding: list[float] | None,
    job_skills_required: list[str],
    job_exp_level: str | None,
    job_embedding: list[float] | None,
    job_posted_date: datetime | None,
    user_interactions: list[dict] | None = None,
) -> dict:
    """
    Compute the final match score (0-100) using all three layers.

    Returns dict with:
      - matchScore: int (0-100)
      - reasons: list[str] — why the user matches
      - missingSkills: list[str] — skills the job requires but user lacks
      - skills: list[str] — matching skills
    """
    # Normalize both skill sets for comparison
    resume_skill_set = set(normalize_skills(resume_skills))
    job_skill_set = set(normalize_skills(job_skills_required))

    # ── Layer 1: Keyword match ──
    kw_score = keyword_match_score(
        resume_skill_set,
        job_skill_set,
        resume_exp_years,
        job_exp_level,
    )

    # ── Layer 2: Semantic match ──
    sem_score = semantic_similarity(resume_embedding, job_embedding)

    # ── Layer 3: Personalization ──
    pers_score = personalization_score(
        user_interactions or [],
        job_embedding,
    )

    # ── Weighted combination ──
    raw_score = (
        WEIGHTS["keyword"] * kw_score
        + WEIGHTS["semantic"] * sem_score
        + WEIGHTS["personalization"] * pers_score
    )

    # ── Recency boost ──
    recency_boost = 0.0
    if job_posted_date:
        now = datetime.now(timezone.utc)
        if job_posted_date.tzinfo is None:
            job_posted_date = job_posted_date.replace(tzinfo=timezone.utc)
        job_age_days = (now - job_posted_date).days
        recency_boost = min(0.1, max(0, (7 - job_age_days) / 70))

    final_score = round(min(100, (raw_score + recency_boost) * 100), 1)

    # ── Build reasons ──
    matching = get_matching_skills(resume_skill_set, job_skill_set)
    missing = get_missing_skills(resume_skill_set, job_skill_set)

    reasons = []
    if matching:
        top_matches = matching[:4]
        reasons.append(f"{', '.join(get_display_name(s) for s in top_matches)} expertise")
    if resume_exp_years > 0:
        reasons.append(f"{resume_exp_years:.0f}+ years experience")
    if kw_score > 0.6:
        reasons.append("Strong skill alignment")
    if sem_score > 0.7:
        reasons.append("Highly relevant background")

    return {
        "matchScore": int(final_score),
        "reasons": reasons if reasons else ["Profile under review"],
        "missingSkills": [get_display_name(s) for s in missing[:5]],
        "skills": [get_display_name(s) for s in matching],
    }
