from fastapi import FastAPI
from api.routes_evaluate import router as eval_router
from api.routes_graph import router as graph_router
from version.metadata import API_VERSION

app = FastAPI(title="Scriptwise Evaluator", version=API_VERSION)

app.include_router(eval_router, prefix="/api")
app.include_router(graph_router)  # /graph/view
