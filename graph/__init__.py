# backend/graph/__init__.py

"""
Graph package.

Exports the entrypoint for building the LangGraph app.
"""

from .graph_builder import build_graph

__all__ = ["build_graph"]
