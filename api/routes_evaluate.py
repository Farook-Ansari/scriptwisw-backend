from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from models.io_models import ScriptInput, EvaluationResponse, ParameterResult, OverallResult
from graph.graph_builder import build_graph

router = APIRouter()
app_graph = build_graph()

@router.get("/graph-view", response_class=HTMLResponse)
async def graph_view():
    mermaid = app_graph.get_graph().draw_mermaid()
    return f"...html with {mermaid}..."

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(script: ScriptInput):
    try:
        state_in = {
            "title": script.title,
            "logline": script.logline,
            "genre": script.genre,
            "content": script.content,
        }
        state_out = await app_graph.ainvoke(state_in)

        # map state_out["parameters"] and overall fields → EvaluationResponse
        ...
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
