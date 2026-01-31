# Simple Chat Example

A minimal chat application demonstrating how to use pygentic-ai.

## Files

- **`app.py`**: Direct agent usage with chat loop (simple, fast)
- **`workflow_example.py`**: Full workflow with routing, guardrails, translation

## Setup

1. Install dependencies:

```bash
# Using pip
pip install pygentic-ai

# Or using uv
uv sync
```

2. Set your API key:

```bash
export OPENAI_API_KEY="sk-..."
```

Or create a `.env` file (copy from `.env.example`).

3. Run the app:

```bash
# With pip
python app.py

# With uv
uv run app.py

# Or use the workflow example
uv run workflow_example.py
```

## What This Example Shows

### 1. Creating a Factory

The `AgentFactory` class configures and initializes multiple agents:

```python
class AgentFactory:
    @staticmethod
    async def create_manager(config: AppConfig) -> AgentManager:
        manager = AgentManager()

        # Factory registers agents with configuration
        manager.register("agent", ReasoningAgent, api_key=config.api_key, ...)
        manager.register("guardrails", GuardrailsAgent, ...)
        manager.register("translator", SimpleTranslatorWorker, ...)

        await manager.initialize()
        return manager
```

### 2. Using the Agent Directly (`app.py`)

Simple chat loop without workflow - best for quick prototyping:

```python
agent = manager.get("agent")
result = await agent.generate_response(user_input, chat_history)
print(result.output)
```

**Pros**: Fast, simple, direct control
**Cons**: No automatic routing, guardrails, or translation

### 3. Using Full Workflow (`workflow_example.py`)

With the pre-built workflow - production-ready:

```python
# manager.to_deps() automatically includes all registered agents
result = await user_assistant_graph.run(
    {"message": user_input},
    manager.to_deps(chat_history=chat_history)
)
```

**Pros**: Automatic routing, guardrails, translation
**Cons**: More complex, slightly slower

The workflow automatically:
- Routes messages (classifies intent)
- Applies content guardrails
- Translates output to target language
- Handles refusals

## Key Concepts

- **Factory Pattern**: Centralized configuration of agents
- **AgentManager**: Register and manage multiple agents
- **Chat History**: Maintain conversation context
- **Usage Limits**: Control token usage

## Customization

You can modify `AppConfig` to:
- Change the model (e.g., "gpt-4o", "claude-3-5-sonnet-20241022")
- Set different language
- Adjust token limits
- Add more agents

## Dependencies

This example requires:
- Python 3.12+
- pygentic-ai >= 0.1.0

All dependencies are managed in `pyproject.toml`.
