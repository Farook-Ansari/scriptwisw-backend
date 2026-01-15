from typing import Dict

from ..state import GraphState
from models.evaluation_models import (
    OverallEvaluation,
    EvaluationVerdict,
    ParameterEvaluation,
)


def aggregate_scores(state: GraphState) -> GraphState:
    """
    Collect all per-parameter evaluations, compute overall scores + verdict,
    and stash them back onto the state.
    """

    param_results: Dict[str, ParameterEvaluation] = (
        state.get("parameter_results") or {}
    )

    # If something went wrong upstream, fail gracefully
    if not param_results:
        overall = OverallEvaluation(
            average_score=0.0,
            weighted_score=None,
            verdict=EvaluationVerdict.POOR,
            parameter_evaluations={},
            metadata={"reason": "No parameter evaluations produced"},
        )
        state["overall"] = overall
        state["overall_average_score"] = 0.0
        state["overall_weighted_score"] = None
        state["overall_verdict"] = overall.verdict.value
        return state

    scores = [p.raw_score for p in param_results.values()]
    avg_score = sum(scores) / len(scores)

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

    # Store back onto graph state
    state["overall"] = overall
    state["overall_average_score"] = avg_score
    state["overall_weighted_score"] = None
    state["overall_verdict"] = verdict.value

    return state


# Backwards-compatible alias (just in case anything imports this name)
aggregator_node = aggregate_scores
