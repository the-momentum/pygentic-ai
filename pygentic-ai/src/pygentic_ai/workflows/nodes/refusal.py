"""Refusal node for handling rejected requests."""

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from pygentic_ai.static.default_msgs import REFUSAL_GENERIC
from pygentic_ai.workflows.state import WorkflowState


@dataclass
class RefuseNode(BaseNode[WorkflowState, dict, str]):
    """Node that returns a refusal response with the reason.

    This node is used when the router classifies a message as requiring refusal
    (e.g., attempts to jailbreak the system).
    """

    async def run(self, ctx: GraphRunContext[WorkflowState, dict]) -> End[str]:
        language = ctx.deps.get("language", "english")
        refusal_reason = ctx.state.refusal_info.refusal_reason if ctx.state.refusal_info else "Unknown reason"
        response = REFUSAL_GENERIC[language].format(refusal_reason=refusal_reason)
        return End(response)
