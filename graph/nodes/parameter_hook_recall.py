# backend/graph/nodes/parameter_hook_recall.py

from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from services.llm_service import get_llm
from prompts.parameter_rubrics import (
    HOOK_RECALL_SYSTEM_PROMPT,
    HOOK_RECALL_USER_PROMPT,
)
from models.evaluation_models import ParameterEvaluation
from graph.state import GraphState


def evaluate_hook_recall(state: GraphState) -> dict:
    """
    Node for: MARKET HOOK & RECALL VALUE

    Uses HOOK_RECALL_* prompts and writes a ParameterEvaluation into:
        state["parameter_results"]["hook_recall"]
    """

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", HOOK_RECALL_SYSTEM_PROMPT),
            ("user", HOOK_RECALL_USER_PROMPT),
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
        # Fallback if LLM call fails
        fallback = ParameterEvaluation(
            parameter_id="hook_recall",
            parameter_name="Market Hook & Recall Value",
            raw_score=0.0,
            normalized_score=0.0,
            confidence=0.0,
            reasoning=f"Model failure while evaluating hook & recall: {exc}",
            evidence=[],
        )
        return {"parameter_results": {"hook_recall": fallback}}

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
        parameter_id="hook_recall",
        parameter_name="Market Hook & Recall Value",
        raw_score=score,
        normalized_score=score / 10.0,
        confidence=confidence,
        reasoning=reasoning,
        evidence=evidence,
    )

    return {"parameter_results": {"hook_recall": param_eval}}


# Optional alias if you ever want node-style naming
hook_recall_node = evaluate_hook_recall
