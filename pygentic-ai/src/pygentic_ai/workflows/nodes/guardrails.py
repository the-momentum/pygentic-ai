"""Guardrails node for output validation and formatting."""

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from pygentic_ai.workflows.state import WorkflowState


@dataclass
class GuardrailsNode(BaseNode[WorkflowState, dict, str]):
    """Node that validates and reformats the generated response.

    This is typically the final processing node before returning the response.
    It applies guardrails to ensure the response meets formatting and content guidelines.
    """

    async def run(self, ctx: GraphRunContext[WorkflowState, dict]) -> End[str]:
        guardrails = ctx.deps["guardrails"]
        result = await guardrails.reformat(ctx.state.generated_response)
        return End(result)
