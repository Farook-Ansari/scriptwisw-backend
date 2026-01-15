"""
API version and build information.
"""

API_VERSION = "1.0.0"

BUILD_INFO = {
    "version": API_VERSION,
    "name": "Scriptwise Multiagent Backend",
    "description": "Script evaluation API using LangGraph multi-agent system",
    "author": "Scriptwise Team",
    "python_version": "3.10+",
    "framework": "FastAPI",
    "graph_engine": "LangGraph"
}


def get_version() -> str:
    """Returns the current API version."""
    return API_VERSION


def get_build_info() -> dict:
    """Returns complete build information."""
    return BUILD_INFO
