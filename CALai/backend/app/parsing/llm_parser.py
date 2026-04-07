"""
LLM-based structured resume extraction — uses Gemini API.
Prompt from 02_resume_parsing_engine.md Step 3.
"""

import json
import logging

import google.generativeai as genai

from app.config import get_settings

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """Extract structured data from this resume text. Return ONLY valid JSON with no markdown formatting, no code fences.

{
  "personal_info": {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin_url": "",
    "github_url": ""
  },
  "summary": "",
  "skills": {
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "tools": [],
    "soft_skills": [],
    "other": []
  },
  "experience": [
    {
      "company": "",
      "title": "",
      "location": "",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM or present",
      "description": "",
      "technologies_used": [],
      "achievements": []
    }
  ],
  "education": [
    {
      "institution": "",
      "degree": "",
      "field_of_study": "",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM",
      "gpa": "",
      "relevant_courses": []
    }
  ],
  "projects": [
    {
      "name": "",
      "description": "",
      "technologies": [],
      "url": "",
      "highlights": []
    }
  ],
  "certifications": [
    {
      "name": "",
      "issuer": "",
      "date": "",
      "url": ""
    }
  ],
  "keywords": []
}

Resume Text:
"""


async def parse_with_llm(resume_text: str, sections: dict[str, str] | None = None) -> dict:
    """
    Send resume text to Gemini for structured extraction.
    Falls back to a basic heuristic extraction if LLM is unavailable.
    """
    settings = get_settings()

    if not settings.GEMINI_API_KEY:
        logger.warning("No Gemini API key configured. Using fallback parser.")
        return _fallback_parse(resume_text, sections)

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Build context-enriched prompt
        prompt = EXTRACTION_PROMPT + resume_text[:8000]  # Limit tokens

        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                response_mime_type="application/json",
            ),
        )

        result = json.loads(response.text)
        return result

    except Exception as e:
        logger.error(f"LLM parsing failed: {e}. Using fallback.")
        return _fallback_parse(resume_text, sections)


def _fallback_parse(resume_text: str, sections: dict[str, str] | None = None) -> dict:
    """
    Basic heuristic extraction when LLM is unavailable.
    Extracts what it can from section-detected text.
    """
    sections = sections or {}

    # Extract skills from skills section
    skills_text = sections.get("skills", "")
    raw_skills = []
    if skills_text:
        for line in skills_text.split("\n"):
            # Split by common delimiters
            for delim in [",", "|", "•", "·", ";"]:
                if delim in line:
                    raw_skills.extend(
                        s.strip() for s in line.split(delim) if s.strip() and len(s.strip()) < 50
                    )
                    break
            else:
                cleaned = line.strip().strip("-").strip("•").strip()
                if cleaned and len(cleaned) < 50:
                    raw_skills.append(cleaned)

    # Extract experience entries
    experience = []
    exp_text = sections.get("experience", "")
    if exp_text:
        experience.append({
            "company": "",
            "title": "",
            "location": "",
            "start_date": "",
            "end_date": "",
            "description": exp_text[:500],
            "technologies_used": [],
            "achievements": [],
        })

    # Extract education entries
    education = []
    edu_text = sections.get("education", "")
    if edu_text:
        education.append({
            "institution": "",
            "degree": "",
            "field_of_study": "",
            "start_date": "",
            "end_date": "",
            "gpa": "",
            "relevant_courses": [],
        })

    return {
        "personal_info": {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin_url": "",
            "github_url": "",
        },
        "summary": sections.get("summary", ""),
        "skills": {
            "programming_languages": [],
            "frameworks": [],
            "databases": [],
            "tools": [],
            "soft_skills": [],
            "other": raw_skills,
        },
        "experience": experience,
        "education": education,
        "projects": [],
        "certifications": [],
        "keywords": raw_skills[:20],
    }
