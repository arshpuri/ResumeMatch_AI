"""
Layer 3: Personalization — from 04_recommendation_engine.md.
User behavior signals with time-decay weighting.
"""

import math
from datetime import datetime, timezone

import numpy as np


# Signal weights from blueprint
ACTION_WEIGHTS: dict[str, float] = {
    "apply": 1.0,
    "save": 0.7,
    "click": 0.3,
    "view": 0.2,
    "dismiss": -0.5,
    "unsave": -0.3,
}

# Half-life in days for time decay
ACTION_HALF_LIFE: dict[str, int] = {
    "apply": 30,
    "save": 14,
    "click": 7,
    "view": 7,
    "dismiss": 7,
    "unsave": 7,
}


def compute_decay(interaction_time: datetime, half_life_days: int = 14) -> float:
    """Exponential decay based on time elapsed."""
    now = datetime.now(timezone.utc)
    if interaction_time.tzinfo is None:
        interaction_time = interaction_time.replace(tzinfo=timezone.utc)

    elapsed_days = (now - interaction_time).total_seconds() / 86400.0
    return math.exp(-0.693 * elapsed_days / half_life_days)


def personalization_score(
    user_interactions: list[dict],
    job_embedding: list[float] | None,
) -> float:
    """
    Score based on similarity to past interactions.
    Returns 0.5 (neutral) for new users / cold start.

    user_interactions: list of dicts with 'action', 'timestamp', 'job_embedding' keys
    job_embedding: the candidate job's embedding
    """
    if not user_interactions or job_embedding is None:
        return 0.5  # Cold start: neutral score

    positive_embeddings = []

    for interaction in user_interactions:
        action = interaction.get("action", "")
        timestamp = interaction.get("timestamp")
        emb = interaction.get("job_embedding")

        if emb is None or action not in ACTION_WEIGHTS:
            continue

        weight = ACTION_WEIGHTS[action]
        if weight <= 0:
            continue  # Skip negative signals for preference vector

        half_life = ACTION_HALF_LIFE.get(action, 14)
        if timestamp:
            decay = compute_decay(timestamp, half_life)
        else:
            decay = 0.5

        weighted_emb = np.array(emb) * weight * decay
        positive_embeddings.append(weighted_emb)

    if not positive_embeddings:
        return 0.5

    # Build user preference vector as weighted mean
    user_preference = np.mean(positive_embeddings, axis=0)
    norm = np.linalg.norm(user_preference)
    if norm == 0:
        return 0.5

    user_preference = user_preference / norm
    job_vec = np.array(job_embedding)

    return float(np.dot(user_preference, job_vec))
