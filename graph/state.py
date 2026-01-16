# backend/graph/state.py

from typing import TypedDict, List, Annotated, Any, Dict, Optional
from operator import or_
from models.evaluation_models import ParameterMap, OverallEvaluation


def merge_dicts(left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:
    """Reducer that merges two dicts, with right taking precedence."""
    if left is None:
        left = {}
    if right is None:
        right = {}
    return {**left, **right}


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
    # Uses Annotated with merge_dicts reducer to allow parallel node updates
    # Keyed by parameter_id (e.g. "story_engine", "hook_conceptual_recall", etc.)
    parameter_results: Annotated[ParameterMap, merge_dicts]

    # Aggregated results (set by aggregator node)
    overall: OverallEvaluation
    overall_average_score: float
    overall_weighted_score: Optional[float]
    overall_verdict: str

    # Legacy field names (for backwards compatibility)
    overall_score: float           # 1–10 final score
    verdict_band: str             # e.g. "Strong Recommend", "Consider with Reservations"
    verdict_text: str             # short explanatory band text
    top_strengths: List[str]
    development_areas: List[str]
    global_summary: str           # 3–6 line executive summary

    # Summary node output
    summary: str
        

# Backwards compatibility – if any old code still imports GraphState,
# it will refer to the same structure as EvaluationState.
GraphState = EvaluationState


