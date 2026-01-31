"""Router agent for classifying and routing messages."""

from dataclasses import dataclass
from typing import Callable

from pydantic import BaseModel

from pygentic_ai.engines.base import BaseAgent, BaseAgentDeps
from pygentic_ai.prompts.worker_prompts import get_router_instructions


@dataclass
class RouterDeps(BaseAgentDeps):
    """Dependencies for the router."""

    pass


class RoutingResponse(BaseModel):
    """Structured response from the router.

    Attributes:
        route: The route number (1=conversation, 2=refuse, 3=translate)
        reasoning: Explanation for the routing decision
    """

    route: int
    reasoning: str


class GenericRouter(BaseAgent):
    """Generic message routing using Pydantic AI structured output.

    This router classifies incoming messages and determines how they should
    be handled in the workflow (e.g., standard conversation, refusal, translation).

    Args:
        routing_prompt: Custom routing instructions (optional)
        deps_type: Dependencies type
        **kwargs: Additional BaseAgent arguments

    Example:
        ```python
        router = GenericRouter(verbose=True, api_key="sk-...")
        result = await router.route("Translate this to Spanish: Hello")
        print(result.route)  # 3 (translation)
        print(result.reasoning)  # "User explicitly requested translation"
        ```
    """

    def __init__(
        self,
        routing_prompt: str | None = None,
        deps_type: type[BaseAgentDeps] = RouterDeps,
        **kwargs,
    ) -> None:
        instructions: str | Callable = routing_prompt if routing_prompt is not None else get_router_instructions
        super().__init__(deps_type=deps_type, output_type=RoutingResponse, instructions=instructions, **kwargs)

    async def route(
        self,
        message: str,
        api_key: str | None = None,
        logging: bool = False,
    ) -> RoutingResponse:
        """Route message and return classification.

        Args:
            message: Message to classify
            api_key: API key for the model (unused, kept for compatibility)
            logging: Whether to log the routing decision

        Returns:
            RoutingResponse with route and reasoning
        """
        deps = RouterDeps(language=self.language)
        result = await self.agent.run(user_prompt=message, deps=deps)
        routing = result.output

        # Type narrowing for ty check
        assert isinstance(routing, RoutingResponse), "Expected RoutingResponse from agent"

        if logging or self.verbose:
            print(routing.route, routing.reasoning)

        return routing
