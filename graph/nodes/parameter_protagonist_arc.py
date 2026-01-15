# backend/graph/nodes/parameter_protagonist_arc.py

from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from services.llm_service import get_llm
from prompts.parameter_rubrics import (
    PROTAGONIST_ARC_SYSTEM_PROMPT,
    PROTAGONIST_ARC_USER_PROMPT,
)
from models.evaluation_models import ParameterEvaluation
from graph.state import GraphState


def evaluate_protagonist_arc(state: GraphState) -> GraphState:
    """
    Node for: PROTAGONIST ARC & INTERNAL JOURNEY

    - Uses the PROTAGONIST_ARC rubric + prompts (from prompts/parameter_rubrics.py).
    - Calls the self-hosted LLaMA via get_llm().
    - Writes a ParameterEvaluation into:
        state["parameter_results"]["protagonist_arc"].
    """

    # Ensure param-results container exists
    if "parameter_results" not in state or state["parameter_results"] is None:
        state["parameter_results"] = {}

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PROTAGONIST_ARC_SYSTEM_PROMPT),
            ("user", PROTAGONIST_ARC_USER_PROMPT),
        ]
    )

    parser = JsonOutputParser()
    chain = prompt | llm | parser

    try:
        raw: Dict[str, Any] = chain.invoke(
            {
                "title": state.get("title", ""),
                "logline": state.get("logline", ""),
                "genre": state.get("genre", ""),
                "content": state.get("content", ""),
            }
        )
    except Exception as exc:
        # Fall back to a safe, debuggable result
        fallback = ParameterEvaluation(
            parameter_id="protagonist_arc",
            parameter_name="Protagonist Arc & Internal Journey",
            raw_score=0.0,
            normalized_score=0.0,
            confidence=0.0,
            reasoning=f"Model failure while evaluating protagonist arc: {exc}",
            evidence=[],
        )
        state["parameter_results"]["protagonist_arc"] = fallback
        return state

    # ---- Defensive parsing of LLM JSON ----
    score = raw.get("score", 0.0)
    try:
        score = float(score)
    except Exception:
        score = 0.0
    score = max(0.0, min(10.0, score))

    confidence = raw.get("confidence", 1.0)
    try:
        confidence = float(confidence)
    except Exception:
        confidence = 1.0
    confidence = max(0.0, min(1.0, confidence))

    reasoning = str(raw.get("reasoning", "")).strip()

    evidence_raw = raw.get("evidence") or []
    if isinstance(evidence_raw, list):
        evidence: List[str] = [str(e) for e in evidence_raw]
    else:
        evidence = [str(evidence_raw)]

    param_eval = ParameterEvaluation(
        parameter_id="protagonist_arc",
        parameter_name="Protagonist Arc & Internal Journey",
        raw_score=score,
        normalized_score=score / 10.0,
        confidence=confidence,
        reasoning=reasoning,
        evidence=evidence,
    )

    state["parameter_results"]["protagonist_arc"] = param_eval
    return state
