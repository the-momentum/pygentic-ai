"""Agent workflow definition."""

from pydantic_graph import Graph

from pygentic_ai.workflows.nodes import (
    ClassifyNode,
    GenerateNode,
    GuardrailsNode,
    RefuseNode,
    StartNode,
    TranslateNode,
)

user_assistant_graph = Graph(
    nodes=(StartNode, ClassifyNode, GenerateNode, GuardrailsNode, TranslateNode, RefuseNode),  # type: ignore[arg-type]
    name="UserAssistantWorkflow",
)
