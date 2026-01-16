# backend/graph/nodes/parameter_momentum.py

from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from services.llm_service import get_llm
from prompts.parameter_rubrics import (
    MOMENTUM_SYSTEM_PROMPT,
    MOMENTUM_USER_PROMPT,
)
from models.evaluation_models import ParameterEvaluation
from graph.state import GraphState


def evaluate_momentum(state: GraphState) -> dict:
    """
    Node for: STRUCTURAL MOMENTUM & ESCALATION

    - Uses the MOMENTUM rubric + prompts.
    - Calls the self-hosted LLaMA via get_llm().
    - Writes a ParameterEvaluation into state["parameter_results"]["momentum"].
    """

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", MOMENTUM_SYSTEM_PROMPT),
            ("user", MOMENTUM_USER_PROMPT),
        ]
    )

    chain = prompt | llm | JsonOutputParser()

    # Invoke model
    result: Dict[str, Any] = chain.invoke(
        {
            "title": state.get("title", ""),
            "logline": state.get("logline", ""),
            "genre": state.get("genre", ""),
            "content": state.get("content", ""),
        }
    )

    # Defensive parsing
    score_raw = float(result.get("score", 0.0))
    confidence_raw = float(result.get("confidence", 1.0))
    reasoning = result.get("reasoning", "")
    evidence = result.get("evidence") or []

    # Build internal parameter evaluation object
    param_eval = ParameterEvaluation(
        parameter_id="momentum",
        parameter_name="Structural Momentum & Escalation",
        raw_score=score_raw,
        normalized_score=score_raw / 10.0,
        confidence=confidence_raw,
        reasoning=reasoning,
        evidence=evidence,
    )

    return {"parameter_results": {"momentum": param_eval}}
