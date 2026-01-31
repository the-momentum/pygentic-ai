"""
Simple Chat Application Example

This example demonstrates how to build a basic chat application with pygentic-ai.
It shows:
- Creating a factory to configure agents
- Setting up a simple workflow
- Running the chat loop
"""

import asyncio
import os
from dataclasses import dataclass

from pydantic_ai import UsageLimits

from pygentic_ai import AgentManager
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
        """Create and initialize agent manager with all required agents.

        Args:
            config: Application configuration

        Returns:
            Configured and initialized AgentManager
        """
        manager = AgentManager()

        # Configure usage limits
        usage_limits = UsageLimits(
            output_tokens_limit=config.max_output_tokens,
        )

        # Register main reasoning agent
        manager.register(
            "agent",
            ReasoningAgent,
            api_key=config.api_key,
            llm_model=config.model,
            language=config.language,
            usage_limits=usage_limits,
            verbose=True,
        )

        # Register guardrails agent for safety checks
        manager.register(
            "guardrails",
            GuardrailsAgent,
            api_key=config.api_key,
            llm_model=config.model,
            language=config.language,
            usage_limits=usage_limits,
        )

        # Register translator
        manager.register(
            "translator",
            SimpleTranslatorWorker,
            api_key=config.api_key,
            target_language=config.language,
            usage_limits=usage_limits,
        )

        # Initialize all agents
        await manager.initialize()
        return manager


async def chat_loop(manager: AgentManager):
    """Simple chat loop using the agent."""
    print("Chat started! (type 'quit' to exit)\n")

    chat_history = []
    agent = manager.get("agent")

    while True:
        # Get user input
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        # Generate response
        try:
            result = await agent.generate_response(user_input, chat_history)
            response = str(result.output)

            print(f"Assistant: {response}\n")

            # Update chat history with new messages
            chat_history = result.messages

        except Exception as e:
            print(f"Error: {e}\n")


async def main():
    """Main application entry point."""
    # Load configuration
    config = AppConfig()

    if not config.api_key:
        print("Error: Please set OPENAI_API_KEY environment variable")
        return

    # Create agent manager
    print("Initializing agents...")
    manager = await AgentFactory.create_manager(config)
    print("Ready!\n")

    # Start chat loop
    await chat_loop(manager)


if __name__ == "__main__":
    asyncio.run(main())
