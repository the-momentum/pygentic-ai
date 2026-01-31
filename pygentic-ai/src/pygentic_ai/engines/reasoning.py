"""Reasoning agent for general-purpose AI interactions."""

from dataclasses import dataclass

from pygentic_ai.engines.base import BaseAgent, BaseAgentDeps
from pygentic_ai.prompts.agent_prompts import get_instructions_for_mode
from pygentic_ai.schemas import AgentMode


@dataclass
class ReasoningAgentDeps(BaseAgentDeps):
    """Dependencies for the reasoning agent."""

    pass


class ReasoningAgent(BaseAgent):
    """Reasoning agent with tool usage capabilities.

    This is a general-purpose agent that can reason about problems and
    use tools to gather information before responding.

    Args:
        deps_type: Dependencies type
        **kwargs: Additional BaseAgent arguments

    Example:
        ```python
        from pygentic_ai.engines import ReasoningAgent

        agent = ReasoningAgent(
            api_key="sk-...",
            tool_list=[my_search_tool],
            verbose=True
        )
        result = await agent.generate_response("What's the weather?", [])
        print(result.output)
        ```
    """

    def __init__(
        self,
        deps_type: type[BaseAgentDeps] = ReasoningAgentDeps,
        **kwargs,
    ) -> None:
        instructions = get_instructions_for_mode(AgentMode.GENERAL)
        super().__init__(deps_type=deps_type, instructions=instructions, **kwargs)
