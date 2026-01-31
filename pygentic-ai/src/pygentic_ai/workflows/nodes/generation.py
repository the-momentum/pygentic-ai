"""Generation node for producing agent responses."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic_graph import BaseNode, GraphRunContext

from pygentic_ai.workflows.state import WorkflowState

if TYPE_CHECKING:
    from pygentic_ai.workflows.nodes.guardrails import GuardrailsNode


@dataclass
class GenerateNode(BaseNode[WorkflowState, dict, str]):
    """Node that generates a response using the main agent.

    This node uses the configured agent to generate a response to the
    current message and stores it in the workflow state.
    """

    async def run(self, ctx: GraphRunContext[WorkflowState, dict]) -> "GuardrailsNode":
        from pygentic_ai.workflows.nodes.guardrails import GuardrailsNode

        agent = ctx.deps["agent"]
        chat_history = ctx.deps.get("chat_history", [])
        response = await agent.generate_response(ctx.state.current_message, chat_history)
        ctx.state.generated_response = str(response.output)
        return GuardrailsNode()
