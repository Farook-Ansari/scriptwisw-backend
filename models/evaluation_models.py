"""
Internal parameter and overall evaluation schemas.
"""

from __future__ import annotations

from enum import Enum
from typing import TypedDict, List, Optional, Dict, Any

from pydantic import BaseModel, Field


# ========= High-level verdict enum (for overall use) =========

class EvaluationVerdict(str, Enum):
    """Verdict categories for script evaluation."""
    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_WORK = "needs_work"
    POOR = "poor"


# ========= LangGraph-internal parameter representations =========

class ParameterState(TypedDict):
    """
    Lightweight internal representation of a single parameter evaluation.
    This is what the parameter nodes write into the graph state.

    - score: 1–10 raw score
    - reasoning: short explanation focused on this parameter
    - suggestions: concrete revision ideas for this dimension
    """
    score: float
    reasoning: str
    suggestions: List[str]


class ParameterMap(TypedDict, total=False):
    """
    Map of all parameter IDs to their evaluation state.
    Each of the 10 parameter nodes fills one of these keys.
    """

    # 1. Central Story Engine / Spine
    story_engine: ParameterState

    # 2. Protagonist Goal, Stakes & Opposition
    goal_stakes_opposition: ParameterState

    # 3. Structural Momentum & Scene Economy
    momentum_scene_economy: ParameterState

    # 4. Protagonist Depth & Arc
    protagonist_depth_arc: ParameterState

    # 5. Relationships & Supporting Cast
    relationships_supporting_cast: ParameterState

    # 6. Emotional Resonance & Social Truth
    emotional_resonance_social_truth: ParameterState

    # 7. World Specificity & Cultural Rootedness
    world_specificity_cultural_rootedness: ParameterState

    # 8. Thematic & Cinematic Resonance
    thematic_cinematic_resonance: ParameterState

    # 9. Hook Strength & Conceptual Recall
    hook_conceptual_recall: ParameterState

    # 10. Audience Fit & Market Positioning
    audience_market_positioning: ParameterState


# ========= Richer internal models (optional, for later use) =========

class ParameterEvaluation(BaseModel):
    """
    Rich internal model for an individual parameter evaluation.
    Useful if you later want to persist or expose more metadata
    than the minimal ParameterState.

    - parameter_id: internal key (e.g. "story_engine")
    - parameter_name: human-readable label
    - raw_score: 1–10 score
    - normalized_score: 0–1 normalized score (e.g., raw_score / 10)
    - confidence: model's confidence (if you ever estimate it)
    - reasoning: textual explanation
    - evidence: optional concrete text/line references
    """
    parameter_id: str
    parameter_name: str
    raw_score: float = Field(..., ge=0, le=10)
    normalized_score: float = Field(..., ge=0, le=1)
    confidence: float = Field(default=1.0, ge=0, le=1)
    reasoning: str
    evidence: List[str] = Field(default_factory=list)


class OverallEvaluation(BaseModel):
    """
    Aggregated evaluation result model.

    - average_score: simple mean of parameter scores
    - weighted_score: optional weighted score if you introduce weights
    - verdict: final band/category
    - parameter_evaluations: map of parameter_id -> ParameterEvaluation
    - metadata: extra info (e.g. weights used, timestamp, model name)
    """
    average_score: float
    weighted_score: Optional[float] = None
    verdict: EvaluationVerdict
    parameter_evaluations: Dict[str, ParameterEvaluation]
    metadata: Dict[str, Any] = Field(default_factory=dict)
