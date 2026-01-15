"""
Protagonist Goal, Stakes & Conflict Loop parameter node.

Evaluates whether the script has:
- A clear, active protagonist goal
- Meaningful, escalating stakes
- A robust conflict engine (obstacles, reversals, pressure)
"""

from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from ..state import GraphState
from models.evaluation_models import ParameterEvaluation
from services.llm_service import get_llm


GOAL_STAKES_SYSTEM_PROMPT = """
You are a senior story editor at a major film studio.

Your ONLY task is to evaluate the script's:
- Protagonist goal
- Stakes (personal, relational, societal)
- Ongoing conflict loop / engine

Be clinical and use the full 0–10 range:
- 0–2  = no clear goal, stakes, or conflict; chaos.
- 3–4  = very weak or generic; protagonist mostly reactive.
- 5–6  = functional but not compelling; "does the job" but forgettable.
- 7–8  = strong, active, cinematic goal with real pressure.
- 9–10 = outstanding, premium conflict engine with high emotional pull.
"""


GOAL_STAKES_USER_PROMPT = """
You will be given:
- Title
- Logline
- Genre
- Full synopsis text

Your focus is ONLY:

1. PROTAGONIST GOAL
   - Is the goal specific and active (e.g., "steal the painting by midnight")?
   - Or vague/reactive (e.g., "survive", "figure things out")?
   - Does the protagonist CHOOSE this goal, or just get dragged along?

2. STAKES
   - What happens if they fail — concretely?
   - Are the stakes personal (relationships, identity, guilt), external (job, freedom),
     and/or societal (city, nation, world)?
   - Are the stakes visible and felt throughout the story, or only mentioned in logline?

3. CONFLICT LOOP / PRESSURE
   - Are there escalating obstacles testing the protagonist's goal over time?
   - Is there a clear "try → fail → escalate" rhythm or is it flat/repetitive?
   - Does opposition come from meaningful forces (antagonist, system, inner flaw)?

4. ALIGNMENT BETWEEN GOAL, STAKES & PLOT
   - Do all the big set pieces and turns actually stress-test the central goal?
   - Or do we wander into side quests that could be cut without changing the core?

You MUST return STRICT JSON ONLY, matching this exact schema:

{
  "score": 7.5,
  "confidence": 0.82,
  "reasoning": "2–4 paragraphs of analysis...",
  "evidence": [
    "Concrete evidence quote or paraphrase from the synopsis...",
    "Another specific reference..."
  ]
}

Rules:
- `score` must be a float between 0 and 10.
- `confidence` must be a float between 0 and 1.0 indicating how certain you are.
- `reasoning` must reference specific beats in the story.
- `evidence` must be a list of concrete details, not vague opinions.

Now evaluate this project:

TITLE: {title}
LOGLINE: {logline}
GENRE: {genre}

SYNOPSIS:
{content}
"""


def _call_goal_stakes_model(state: GraphState) -> Dict[str, Any]:
    """
    Internal helper: call LLM and parse JSON result.
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", GOAL_STAKES_SYSTEM_PROMPT),
            ("human", GOAL_STAKES_USER_PROMPT),
        ]
    )

    parser = JsonOutputParser()
    chain = prompt | llm | parser

    return chain.invoke(
        {
            "title": state.get("title", ""),
            "logline": state.get("logline", ""),
            "genre": state.get("genre", ""),
            "content": state.get("content", ""),
        }
    )


def evaluate_goal_stakes(state: GraphState) -> GraphState:
    """
    LangGraph node: evaluate 'Protagonist Goal, Stakes & Conflict Loop'.

    Writes a ParameterEvaluation into:
        state["parameter_results"]["goal_stakes"]
    """
    try:
        result = _call_goal_stakes_model(state)
    except Exception as exc:
        pe = ParameterEvaluation(
            parameter_id="goal_stakes",
            parameter_name="Protagonist Goal, Stakes & Conflict Loop",
            raw_score=0.0,
            normalized_score=0.0,
            confidence=0.0,
            reasoning=f"Model failure while evaluating goal/stakes/conflict: {exc}",
            evidence=[],
        )
        state["parameter_results"]["goal_stakes"] = pe
        return state

    # Defensive parsing
    score = float(result.get("score", 0.0))
    score = max(0.0, min(10.0, score))

    confidence = float(result.get("confidence", 0.7))
    confidence = max(0.0, min(1.0, confidence))

    reasoning = str(result.get("reasoning", "")).strip()
    evidence_raw = result.get("evidence") or []
    if not isinstance(evidence_raw, list):
        evidence: List[str] = [str(evidence_raw)]
    else:
        evidence = [str(x) for x in evidence_raw]

    pe = ParameterEvaluation(
        parameter_id="goal_stakes",
        parameter_name="Protagonist Goal, Stakes & Conflict Loop",
        raw_score=score,
        normalized_score=score / 10.0,
        confidence=confidence,
        reasoning=reasoning,
        evidence=evidence,
    )

    params: Dict[str, ParameterEvaluation] = state.get("parameter_results", {})
    params["goal_stakes"] = pe
    state["parameter_results"] = params

    return state


# Optional alias if anything imports this older style name
goal_stakes_node = evaluate_goal_stakes
