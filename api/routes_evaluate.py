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

        # Debug: print state_out keys and overall_average_score
        print(f"[ROUTES] state_out keys: {list(state_out.keys())}")
        print(f"[ROUTES] overall_average_score: {state_out.get('overall_average_score')}")
        print(f"[ROUTES] overall_verdict: {state_out.get('overall_verdict')}")

        # Map parameter_results to ParameterResult format for API response
        param_results = state_out.get("parameter_results", {})
        parameters_response = {}
        
        for param_id, param_eval in param_results.items():
            # param_eval is a ParameterEvaluation Pydantic model
            parameters_response[param_id] = ParameterResult(
                name=param_eval.parameter_name,
                score=param_eval.raw_score,
                reasoning=param_eval.reasoning,
                suggestions=param_eval.evidence,  # Using evidence as suggestions
            )

        # Build overall result from aggregated state
        overall_result = OverallResult(
            score=state_out.get("overall_average_score", 0.0),
            verdict_band=state_out.get("overall_verdict", "poor"),
            verdict_text=state_out.get("verdict_text", "Evaluation complete"),
            top_strengths=state_out.get("top_strengths", []),
            development_areas=state_out.get("development_areas", []),
            global_summary=state_out.get("summary", ""),  # summary node stores under "summary" key
        )

        return EvaluationResponse(
            title=script.title,
            logline=script.logline,
            genre=script.genre,
            parameters=parameters_response,
            overall=overall_result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
