"""
Layer 1: Keyword matching — from 04_recommendation_engine.md.
Jaccard similarity on normalized skills + experience level fit.
"""


EXP_RANGES: dict[str, tuple[float, float]] = {
    "entry": (0, 2),
    "junior": (0, 2),
    "mid": (2, 5),
    "senior": (5, 10),
    "lead": (8, 20),
    "principal": (10, 25),
    "staff": (8, 20),
}


def keyword_match_score(
    resume_skills: set[str],
    job_skills: set[str],
    resume_exp_years: float,
    job_exp_level: str | None,
) -> float:
    """
    Fast initial filter. Returns 0.0 to 1.0.
    0.7 * skill_overlap (Jaccard) + 0.3 * experience_fit
    """
    # ── Skill overlap (Jaccard similarity) ──
    if not job_skills:
        skill_score = 0.5  # Neutral if no skills listed
    else:
        intersection = resume_skills & job_skills
        union = resume_skills | job_skills
        skill_score = len(intersection) / len(union) if union else 0.0

    # ── Experience level match ──
    if not job_exp_level:
        exp_score = 0.5
    else:
        exp_range = EXP_RANGES.get(job_exp_level.lower(), (0, 20))
        if exp_range[0] <= resume_exp_years <= exp_range[1]:
            exp_score = 1.0
        elif resume_exp_years < exp_range[0]:
            exp_score = max(0, 1 - (exp_range[0] - resume_exp_years) / 3)
        else:
            exp_score = max(0, 1 - (resume_exp_years - exp_range[1]) / 5)

    return 0.7 * skill_score + 0.3 * exp_score


def get_matching_skills(resume_skills: set[str], job_skills: set[str]) -> list[str]:
    """Return the intersection of skills."""
    return sorted(resume_skills & job_skills)


def get_missing_skills(resume_skills: set[str], job_skills: set[str]) -> list[str]:
    """Return skills the job requires but resume doesn't have."""
    return sorted(job_skills - resume_skills)
