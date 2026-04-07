"""
Layer 2: Semantic matching — from 04_recommendation_engine.md.
Uses sentence-transformers (all-MiniLM-L6-v2) for embedding cosine similarity.
Falls back to keyword-only if model not available.
"""

import logging
import numpy as np

logger = logging.getLogger(__name__)

# Lazy-loaded model
_model = None


def _get_model():
    """Lazy load the sentence-transformer model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Loaded sentence-transformers model: all-MiniLM-L6-v2")
        except Exception as e:
            logger.warning(f"Failed to load sentence-transformers: {e}. Semantic matching disabled.")
            _model = "unavailable"
    return _model


def compute_resume_embedding(parsed_resume: dict) -> list[float] | None:
    """
    Create a composite embedding from resume sections.
    Returns list of floats (384-dim) or None if model unavailable.
    """
    model = _get_model()
    if model == "unavailable" or model is None:
        return None

    sections = [
        parsed_resume.get("summary", ""),
    ]

    # Collect skills text
    skills = parsed_resume.get("skills", {})
    if isinstance(skills, dict):
        for category_skills in skills.values():
            if isinstance(category_skills, list):
                sections.append(" ".join(category_skills))
    elif isinstance(skills, list):
        sections.append(" ".join(skills))

    # Concatenate experience descriptions
    for exp in parsed_resume.get("experience", []):
        desc = exp.get("description", "")
        if desc:
            sections.append(desc)

    # Concatenate project descriptions
    for proj in parsed_resume.get("projects", []):
        desc = proj.get("description", "")
        if desc:
            sections.append(desc)

    combined_text = " ".join(filter(None, sections))
    if not combined_text.strip():
        return None

    embedding = model.encode(combined_text, normalize_embeddings=True)
    return embedding.tolist()


def compute_job_embedding(job_title: str, company: str, description: str) -> list[float] | None:
    """Create embedding from job description + requirements."""
    model = _get_model()
    if model == "unavailable" or model is None:
        return None

    text = f"{job_title} at {company}. {description or ''}"
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def semantic_similarity(resume_emb: list[float] | None, job_emb: list[float] | None) -> float:
    """
    Cosine similarity between embeddings.
    Returns 0.5 (neutral) if either embedding is missing.
    """
    if resume_emb is None or job_emb is None:
        return 0.5

    a = np.array(resume_emb)
    b = np.array(job_emb)

    dot = float(np.dot(a, b))
    # Embeddings are already normalized, but just in case:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.5

    return float(dot / (norm_a * norm_b))
