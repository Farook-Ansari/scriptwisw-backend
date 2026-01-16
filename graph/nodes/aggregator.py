from typing import Dict, Any

from ..state import GraphState
from models.evaluation_models import (
    OverallEvaluation,
    EvaluationVerdict,
    ParameterEvaluation,
)


def aggregate_scores(state: GraphState) -> Dict[str, Any]:
    """
    Collect all per-parameter evaluations, compute overall scores + verdict,
    and stash them back onto the state.
    """

    param_results: Dict[str, ParameterEvaluation] = (
        state.get("parameter_results") or {}
    )

    # Debug: print what we received
    print(f"[AGGREGATOR] Received {len(param_results)} parameter results")
    print(f"[AGGREGATOR] Keys: {list(param_results.keys())}")

    # If something went wrong upstream, fail gracefully
    if not param_results:
        print("[AGGREGATOR] No parameter results found, returning 0.0")
        overall = OverallEvaluation(
            average_score=0.0,
            weighted_score=None,
            verdict=EvaluationVerdict.POOR,
            parameter_evaluations={},
            metadata={"reason": "No parameter evaluations produced"},
        )
        return {
            "overall": overall,
            "overall_average_score": 0.0,
            "overall_weighted_score": None,
            "overall_verdict": overall.verdict.value,
        }

    # Extract scores - handle both Pydantic model and dict
    scores = []
    for p in param_results.values():
        if hasattr(p, 'raw_score'):
            scores.append(p.raw_score)
        elif isinstance(p, dict):
            scores.append(p.get('raw_score', 0.0))
        else:
            scores.append(0.0)
    
    avg_score = sum(scores) / len(scores) if scores else 0.0
    print(f"[AGGREGATOR] Scores: {scores}")
    print(f"[AGGREGATOR] Average score: {avg_score}")

    # Simple banding – can be tuned later
    if avg_score >= 8.5:
        verdict = EvaluationVerdict.EXCELLENT
    elif avg_score >= 7.0:
        verdict = EvaluationVerdict.GOOD
    elif avg_score >= 5.0:
        verdict = EvaluationVerdict.NEEDS_WORK
    else:
        verdict = EvaluationVerdict.POOR

    overall = OverallEvaluation(
        average_score=avg_score,
        weighted_score=None,
        verdict=verdict,
        parameter_evaluations=param_results,
        metadata={
            "normalized_average_score": avg_score / 10.0,
            "num_parameters": len(scores),
        },
    )

    # Return only the keys we're modifying
    return {
        "overall": overall,
        "overall_average_score": avg_score,
        "overall_weighted_score": None,
        "overall_verdict": verdict.value,
    }


# Backwards-compatible alias (just in case anything imports this name)
aggregator_node = aggregate_scores

