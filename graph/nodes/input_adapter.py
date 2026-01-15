# backend/graph/nodes/input_adapter.py

from ..state import GraphState


def input_adapter(state: GraphState) -> GraphState:
    """
    Normalise incoming payload into a full GraphState.

    This is the first node in the graph. It:
    - Ensures required keys exist on the state
    - Initialises the parameter_results dict where all
      per-parameter evaluations will be stored.
    """

    # Basic fields from the request
    state.setdefault("title", "")
    state.setdefault("logline", "")
    state.setdefault("genre", "")
    state.setdefault("content", "")

    # Dict that all parameter nodes will fill:
    # parameter_id -> ParameterEvaluation model (as dict)
    if "parameter_results" not in state or state["parameter_results"] is None:
        state["parameter_results"] = {}

    # Optional: initialise overall fields so they always exist
    state.setdefault("overall_average_score", 0.0)
    state.setdefault("overall_weighted_score", None)
    state.setdefault("overall_verdict", None)
    state.setdefault("overall_feedback", "")

    return state


# Optional alias if you ever want to import it with the *_node naming style
input_adapter_node = input_adapter
