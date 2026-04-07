"""
Section header detection — from 02_resume_parsing_engine.md Step 2.
Regex-based section header detection for education, experience, skills, etc.
"""

SECTION_HEADERS: dict[str, list[str]] = {
    "summary": ["summary", "objective", "about me", "profile", "about", "professional summary"],
    "experience": [
        "experience", "work history", "employment", "professional experience",
        "work experience", "career history", "professional background",
    ],
    "education": [
        "education", "academic", "qualification", "degree",
        "academic background", "educational background",
    ],
    "skills": [
        "skills", "technical skills", "competencies", "technologies",
        "core competencies", "areas of expertise", "proficiencies",
        "technical proficiencies", "tools & technologies",
    ],
    "projects": [
        "projects", "portfolio", "academic projects",
        "personal projects", "key projects",
    ],
    "certifications": [
        "certifications", "certificates", "licenses",
        "professional certifications", "credentials",
    ],
    "awards": ["awards", "honors", "achievements", "recognition"],
    "publications": ["publications", "papers", "research"],
    "languages": ["languages", "language proficiency"],
    "interests": ["interests", "hobbies", "activities"],
}


def detect_sections(text: str) -> dict[str, str]:
    """
    Split raw resume text into sections based on header detection.
    Returns a dict mapping section names to their text content.
    """
    lines = text.split("\n")
    current_section = "unknown"
    sections: dict[str, list[str]] = {}

    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        # Check if this line is a section header
        is_header = False
        if stripped and len(lower) < 50:
            for section, keywords in SECTION_HEADERS.items():
                if any(kw == lower or lower.startswith(kw + ":") or lower.startswith(kw + " -") for kw in keywords):
                    current_section = section
                    is_header = True
                    break

        if not is_header and stripped:
            sections.setdefault(current_section, []).append(stripped)

    return {k: "\n".join(v) for k, v in sections.items()}
