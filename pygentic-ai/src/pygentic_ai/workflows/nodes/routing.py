"""Routing/Classification node for determining message handling."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic_graph import BaseNode, GraphRunContext

from pygentic_ai.schemas.agent import TaskType
from pygentic_ai.workflows.state import WorkflowState

if TYPE_CHECKING:
    from pygentic_ai.workflows.nodes.generation import GenerateNode
    from pygentic_ai.workflows.nodes.refusal import RefuseNode
    from pygentic_ai.workflows.nodes.translation import TranslateNode


@dataclass
class ClassifyNode(BaseNode[WorkflowState, dict, str]):
    """Node that classifies the message and routes to appropriate handler.

    This node uses the router agent to classify the incoming message and
    determines which node should handle it next (generation, refusal, or translation).
    """

    async def run(self, ctx: GraphRunContext[WorkflowState, dict]) -> "GenerateNode | RefuseNode | TranslateNode":
        from pygentic_ai.workflows.nodes.generation import GenerateNode
        from pygentic_ai.workflows.nodes.refusal import RefuseNode
        from pygentic_ai.workflows.nodes.translation import TranslateNode

        router = ctx.deps["router"]
        classification = await router.route(ctx.state.current_message)

        if classification.route == TaskType.refuse.value:
            ctx.state.set_refusal(ctx.state.current_message, classification.reasoning)
            return RefuseNode()

        ctx.state.task_type = TaskType(classification.route)

        if classification.route == TaskType.translate.value:
            return TranslateNode()

        return GenerateNode()
