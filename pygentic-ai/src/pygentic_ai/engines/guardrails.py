"""Guardrails agent for output validation and reformatting."""

from dataclasses import dataclass

from pygentic_ai.engines.base import BaseAgent, BaseAgentDeps
from pygentic_ai.prompts.worker_prompts import get_guardrails_instructions


@dataclass
class GuardrailsDeps(BaseAgentDeps):
    """Dependencies for the guardrails agent."""

    pass


class GuardrailsAgent(BaseAgent):
    """Output reformatter and validator using Pydantic AI.

    This agent validates and reformats generated output to ensure it meets
    formatting guidelines, length limits, and content policies.

    Args:
        deps_type: Dependencies type
        **kwargs: Additional BaseAgent arguments

    Example:
        ```python
        guardrails = GuardrailsAgent(api_key="sk-...", language="english")
        result = await guardrails.reformat(
            "Here is a very long response that needs reformatting..."
        )
        ```
    """

    def __init__(
        self,
        deps_type: type[BaseAgentDeps] = GuardrailsDeps,
        **kwargs,
    ) -> None:
        super().__init__(deps_type=deps_type, instructions=get_guardrails_instructions, **kwargs)

    async def reformat(
        self,
        message: str,
        api_key: str | None = None,
        soft_word_limit: int = 250,
    ) -> str:
        """Reformat and validate output message.

        Args:
            message: Message to reformat
            api_key: API key for the model (unused, kept for compatibility)
            soft_word_limit: Maximum word count

        Returns:
            Reformatted message
        """
        if self.verbose:
            print(f"Formatting: \n -------- \n *Input* -> {message}")

        deps = GuardrailsDeps(language=self.language)

        result = await self.agent.run(
            user_prompt=message,
            deps=deps,
        )

        formatted_message = str(result.output)

        if self.verbose:
            print(f"\n *Output* -> {formatted_message}")

        return formatted_message

    # Alias for backward compatibility
    refformat = reformat
