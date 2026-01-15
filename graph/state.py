# backend/graph/state.py

from typing import TypedDict, List
from models.evaluation_models import ParameterMap


class EvaluationState(TypedDict, total=False):
    """
    Shared LangGraph state passed between nodes.

    This is the single source of truth for what flows through the graph.
    """

    # Raw input
    title: str
    logline: str
    genre: str
    content: str

    # Per-parameter results, filled by the 10 parameter agents
    # Keyed by parameter_id (e.g. "story_engine", "hook_conceptual_recall", etc.)
    parameters: ParameterMap

    # Aggregated / final results
    overall_score: float           # 1–10 final score
    verdict_band: str             # e.g. "Strong Recommend", "Consider with Reservations"
    verdict_text: str             # short explanatory band text
    top_strengths: List[str]
    development_areas: List[str]
    global_summary: str           # 3–6 line executive summary
        

# Backwards compatibility – if any old code still imports GraphState,
# it will refer to the same structure as EvaluationState.
GraphState = EvaluationState
