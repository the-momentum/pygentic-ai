"""Translation node for translating messages."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic_graph import BaseNode, GraphRunContext

from pygentic_ai.workflows.state import WorkflowState

if TYPE_CHECKING:
    from pygentic_ai.workflows.nodes.guardrails import GuardrailsNode


@dataclass
class TranslateNode(BaseNode[WorkflowState, dict, str]):
    """Node that translates text to target language.

    Uses the translator agent to translate the current message to the
    specified target language.
    """

    async def run(self, ctx: GraphRunContext[WorkflowState, dict]) -> "GuardrailsNode":
        from pygentic_ai.workflows.nodes.guardrails import GuardrailsNode

        translator = ctx.deps["translator"]
        target_lang = ctx.deps.get("target_language", "english")

        result = await translator.translate(ctx.state.current_message, target_lang)

        ctx.state.generated_response = result
        return GuardrailsNode()
