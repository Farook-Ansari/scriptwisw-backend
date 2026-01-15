# backend/graph/nodes/summary.py

from typing import Dict, List

from langchain_core.prompts import ChatPromptTemplate

from services.llm_service import get_llm
from prompts.base_templates import SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_PROMPT
from models.evaluation_models import ParameterEvaluation, OverallEvaluation
from graph.state import GraphState


def _format_parameter_block(param_results: Dict[str, ParameterEvaluation]) -> str:
    """
    Turn parameter_evaluations into a compact text block for the summary LLM.
    """
    if not param_results:
        return "No parameter evaluations were produced."

    lines: List[str] = []
    for param_id, peval in param_results.items():
        lines.append(
            f"- {peval.parameter_name} ({param_id}): "
            f"score {peval.raw_score:.1f}/10, "
            f"confidence {peval.confidence:.2f}. "
            f"Reasoning: {peval.reasoning}"
        )
    return "\n".join(lines)


def _format_overall_block(overall: OverallEvaluation | None) -> str:
    if overall is None:
        return "No overall evaluation available."

    verdict_label = getattr(overall.verdict, "value", str(overall.verdict))
    parts = [
        f"Average score: {overall.average_score:.2f}/10.",
        f"Verdict: {verdict_label}.",
    ]
    if overall.weighted_score is not None:
        parts.append(f"Weighted score: {overall.weighted_score:.2f}/10.")
    return " ".join(parts)


def summarize_evaluation(state: GraphState) -> GraphState:
    """
    Final node: generate a human-readable coverage-style summary
    from parameter-level scores + overall evaluation.
    """

    llm = get_llm()

    parameter_results: Dict[str, ParameterEvaluation] = state.get(
        "parameter_results", {}
    ) or {}

    overall: OverallEvaluation | None = state.get("overall_evaluation")

    parameter_block = _format_parameter_block(parameter_results)
    overall_block = _format_overall_block(overall)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SUMMARY_SYSTEM_PROMPT),
            ("user", SUMMARY_USER_PROMPT),
        ]
    )

    chain = prompt | llm

    try:
        result = chain.invoke(
            {
                "title": state.get("title", ""),
                "logline": state.get("logline", ""),
                "genre": state.get("genre", ""),
                "parameter_block": parameter_block,
                "overall_block": overall_block,
            }
        )
        summary_text = getattr(result, "content", str(result))
    except Exception as exc:
        summary_text = f"Summary generation failed: {exc}"

    # Store for API layer to return (e.g. mapped into EvaluationResponse)
    state["summary"] = summary_text
    return state
