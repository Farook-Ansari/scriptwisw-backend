from langgraph.graph import StateGraph, START, END

from .state import GraphState
from .nodes import (
    input_adapter,
    evaluate_story_engine,
    evaluate_goal_stakes,
    evaluate_momentum,
    evaluate_protagonist_arc,
    evaluate_relationships,
    evaluate_emotional_truth,
    evaluate_world_specificity,
    evaluate_theme_cinema,
    evaluate_hook_recall,
    evaluate_audience_market,
    aggregate_scores,
    summarize_evaluation,
)


def build_graph():
    workflow = StateGraph(GraphState)

    # Register nodes
    workflow.add_node("input_adapter", input_adapter)
    workflow.add_node("story_engine", evaluate_story_engine)
    workflow.add_node("goal_stakes", evaluate_goal_stakes)
    workflow.add_node("momentum", evaluate_momentum)
    workflow.add_node("protagonist_arc", evaluate_protagonist_arc)
    workflow.add_node("relationships", evaluate_relationships)
    workflow.add_node("emotional_truth", evaluate_emotional_truth)
    workflow.add_node("world_specificity", evaluate_world_specificity)
    workflow.add_node("theme_cinema", evaluate_theme_cinema)
    workflow.add_node("hook_recall", evaluate_hook_recall)
    workflow.add_node("audience_market", evaluate_audience_market)
    workflow.add_node("aggregator", aggregate_scores)
    workflow.add_node("summary", summarize_evaluation)

    # Wiring: input_adapter → all parameter agents (in parallel)
    workflow.add_edge(START, "input_adapter")

    parameter_nodes = [
        "story_engine",
        "goal_stakes",
        "momentum",
        "protagonist_arc",
        "relationships",
        "emotional_truth",
        "world_specificity",
        "theme_cinema",
        "hook_recall",
        "audience_market",
    ]

    for node_name in parameter_nodes:
        workflow.add_edge("input_adapter", node_name)
        workflow.add_edge(node_name, "aggregator")

    # Aggregator → summary → END
    workflow.add_edge("aggregator", "summary")
    workflow.add_edge("summary", END)

    return workflow.compile()
