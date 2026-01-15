# backend/mermaid/mermaid_graph.py

"""
Helpers to render the LangGraph workflow as Mermaid text.
"""

from graph.graph_builder import build_graph


def get_mermaid_diagram() -> str:
    """
    Build the evaluation graph and return its Mermaid representation.
    """
    workflow = build_graph()
    return workflow.get_graph().draw_mermaid()
