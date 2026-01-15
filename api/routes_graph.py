# backend/api/routes_graph.py

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from mermaid import get_mermaid_diagram

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/view", response_class=HTMLResponse)
async def view_graph():
    """
    Render the evaluation LangGraph as a Mermaid diagram in HTML.
    """
    mermaid_syntax = get_mermaid_diagram()

    html_content = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Scriptwise Evaluation Graph</title>
        <meta charset="utf-8" />
        <script type="module">
          import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
          mermaid.initialize({{ startOnLoad: true }});
        </script>
      </head>
      <body>
        <h2>Scriptwise Multi-Agent Evaluation Graph</h2>
        <div class="mermaid">
        {mermaid_syntax}
        </div>
      </body>
    </html>
    """
    return html_content
