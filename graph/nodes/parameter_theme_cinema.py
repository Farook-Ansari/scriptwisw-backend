# backend/graph/nodes/parameter_theme_cinema.py

from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from services.llm_service import get_llm
from prompts.parameter_rubrics import (
    THEME_CINEMA_SYSTEM_PROMPT,
    THEME_CINEMA_USER_PROMPT,
)
from models.evaluation_models import ParameterEvaluation
from graph.state import GraphState


def evaluate_theme_cinema(state: GraphState) -> dict:
    """
    Node for: THEME EXPRESSION & CINEMATIC DRAMATISATION

    Uses THEME_CINEMA_* prompts and writes a ParameterEvaluation into:
        state["parameter_results"]["theme_cinema"]
    """

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", THEME_CINEMA_SYSTEM_PROMPT),
            ("user", THEME_CINEMA_USER_PROMPT),
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
        # Safe fallback if model call explodes
        fallback = ParameterEvaluation(
            parameter_id="theme_cinema",
            parameter_name="Theme & Cinematic Expression",
            raw_score=0.0,
            normalized_score=0.0,
            confidence=0.0,
            reasoning=f"Model failure while evaluating theme & cinema: {exc}",
            evidence=[],
        )
        return {"parameter_results": {"theme_cinema": fallback}}

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
        parameter_id="theme_cinema",
        parameter_name="Theme & Cinematic Expression",
        raw_score=score,
        normalized_score=score / 10.0,
        confidence=confidence,
        reasoning=reasoning,
        evidence=evidence,
    )

    return {"parameter_results": {"theme_cinema": param_eval}}
