from services.llm_service import get_llm
from prompts.parameter_rubrics import (
    STORY_ENGINE_SYSTEM_PROMPT,
    STORY_ENGINE_USER_PROMPT,
)
from models.evaluation_models import ParameterEvaluation
from graph.state import GraphState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def evaluate_story_engine(state: GraphState) -> GraphState:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", STORY_ENGINE_SYSTEM_PROMPT),
            ("user", STORY_ENGINE_USER_PROMPT),
        ]
    )
    chain = prompt | llm | JsonOutputParser()

    result = chain.invoke(
        {
            "title": state.get("title", ""),
            "logline": state.get("logline", ""),
            "genre": state.get("genre", ""),
            "content": state.get("content", ""),
        }
    )

    param_eval = ParameterEvaluation(
        parameter_id="story_engine",
        parameter_name="Central Story Engine",
        raw_score=float(result["score"]),
        normalized_score=float(result["score"]) / 10.0,
        confidence=float(result.get("confidence", 1.0)),
        reasoning=result["reasoning"],
        evidence=result.get("evidence", []),
    )

    state["parameter_results"]["story_engine"] = param_eval
    return state
