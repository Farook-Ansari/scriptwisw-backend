# backend/graph/nodes/parameter_emotional_truth.py

from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from services.llm_service import get_llm
from prompts.parameter_rubrics import (
    EMOTIONAL_TRUTH_SYSTEM_PROMPT,
    EMOTIONAL_TRUTH_USER_PROMPT,
)
from models.evaluation_models import ParameterEvaluation
from graph.state import GraphState


def evaluate_emotional_truth(state: GraphState) -> GraphState:
    """
    Node for: EMOTIONAL & SOCIAL TRUTH

    - Uses the EMOTIONAL_TRUTH rubric + prompts (from prompts/parameter_rubrics.py).
    - Calls the self-hosted LLaMA via get_llm().
    - Writes a ParameterEvaluation into:
        state["parameter_results"]["emotional_truth"].
    """

    # Ensure param-results container exists
    if "parameter_results" not in state or state["parameter_results"] is None:
        state["parameter_results"] = {}

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", EMOTIONAL_TRUTH_SYSTEM_PROMPT),
            ("user", EMOTIONAL_TRUTH_USER_PROMPT),
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
        # Safe fallback if the LLM call fails
        fallback = ParameterEvaluation(
            parameter_id="emotional_truth",
            parameter_name="Emotional & Social Truth",
            raw_score=0.0,
            normalized_score=0.0,
            confidence=0.0,
            reasoning=f"Model failure while evaluating emotional truth: {exc}",
            evidence=[],
        )
        state["parameter_results"]["emotional_truth"] = fallback
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
        parameter_id="emotional_truth",
        parameter_name="Emotional & Social Truth",
        raw_score=score,
        normalized_score=score / 10.0,
        confidence=confidence,
        reasoning=reasoning,
        evidence=evidence,
    )

    state["parameter_results"]["emotional_truth"] = param_eval
    return state
