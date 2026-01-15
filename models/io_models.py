from typing import Dict, List
from pydantic import BaseModel


class ScriptInput(BaseModel):
    title: str
    logline: str
    content: str
    genre: str


class ParameterResult(BaseModel):
    """
    One evaluated parameter (one of the 10 axes).
    """
    name: str              # Human-readable label, e.g. "Story Engine & Structural Spine"
    score: float           # 1–10
    reasoning: str         # Focused analysis for this parameter
    suggestions: List[str] # Concrete improvement suggestions


class OverallResult(BaseModel):
    """
    Aggregated overall rating + global notes.
    """
    score: float
    verdict_band: str
    verdict_text: str
    top_strengths: List[str]
    development_areas: List[str]
    global_summary: str


class EvaluationResponse(BaseModel):
    """
    Full API response for /evaluate.
    """
    title: str
    logline: str
    genre: str

    # key = internal parameter id, value = detailed result
    parameters: Dict[str, ParameterResult]

    # overall blended result
    overall: OverallResult
