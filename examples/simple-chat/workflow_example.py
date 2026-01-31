"""
Simple Chat with Workflow Example

This example shows how to use the pre-built workflow instead of calling agent directly.
"""

import asyncio
import os
from dataclasses import dataclass

from pydantic_ai import UsageLimits

from pygentic_ai import AgentManager, user_assistant_graph
from pygentic_ai.engines import ReasoningAgent, GuardrailsAgent, SimpleTranslatorWorker


@dataclass
class AppConfig:
    """Application configuration."""

    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = "gpt-4o-mini"
    language: str = "english"
    max_output_tokens: int = 2000


class AgentFactory:
    """Factory for creating and configuring agents."""

    @staticmethod
    async def create_manager(config: AppConfig) -> AgentManager:
        """Create and initialize agent manager with all required agents."""
        manager = AgentManager()

        usage_limits = UsageLimits(output_tokens_limit=config.max_output_tokens)

        # Register agents - factory handles all configuration
        manager.register(
            "agent",
            ReasoningAgent,
            api_key=config.api_key,
            llm_model=config.model,
            language=config.language,
            usage_limits=usage_limits,
            verbose=True,
        )

        manager.register(
            "guardrails",
            GuardrailsAgent,
            api_key=config.api_key,
            llm_model=config.model,
            language=config.language,
            usage_limits=usage_limits,
        )

        manager.register(
            "translator",
            SimpleTranslatorWorker,
            api_key=config.api_key,
            target_language=config.language,
            usage_limits=usage_limits,
        )

        await manager.initialize()
        return manager


async def chat_loop(manager: AgentManager):
    """Chat loop using workflow."""
    print("Chat with workflow started! (type 'quit' to exit)\n")

    chat_history = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            # Run workflow - manager.to_deps() includes all registered agents
            from pygentic_ai.workflows.nodes import StartNode

            result = await user_assistant_graph.run(
                StartNode(),  # type: ignore
                state={"message": user_input},  # type: ignore
                deps=manager.to_deps(chat_history=chat_history),  # type: ignore
            )

            print(f"Assistant: {result}\n")

            # Note: workflow result is already processed (translated, guardrailed)
            # You may need to extract chat_history from result if workflow returns it

        except Exception as e:
            print(f"Error: {e}\n")


async def main():
    """Main application using workflow."""
    config = AppConfig()

    if not config.api_key:
        print("Error: Please set OPENAI_API_KEY environment variable")
        return

    print("Initializing agents...")
    manager = await AgentFactory.create_manager(config)
    print("Ready!\n")

    await chat_loop(manager)


if __name__ == "__main__":
    asyncio.run(main())
