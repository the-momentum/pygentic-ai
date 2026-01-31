"""Base/Start node for workflows."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic_graph import BaseNode, GraphRunContext

from pygentic_ai.workflows.state import WorkflowState

if TYPE_CHECKING:
    from pygentic_ai.workflows.nodes.routing import ClassifyNode


@dataclass
class StartNode(BaseNode[WorkflowState, dict, str]):
    """Initial node that initializes workflow state with user message.

    This node should be the entry point for most workflows. It extracts
    the user message from dependencies and stores it in the workflow state.

    Example:
        ```python
        from pydantic_graph import Graph
        from pygentic_ai.workflows.nodes import StartNode, ClassifyNode

        workflow = Graph(
            nodes=(StartNode, ClassifyNode, ...),
            name="MyWorkflow"
        )
        ```
    """

    async def run(self, ctx: GraphRunContext[WorkflowState, dict]) -> "ClassifyNode":
        from pygentic_ai.workflows.nodes.routing import ClassifyNode

        ctx.state.current_message = ctx.deps["message"]
        return ClassifyNode()
