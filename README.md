# pygentic-ai

A meta-framework for building agentic workflows with Pydantic AI.

> **⚠️ Early Alpha**: This library is in active development. The API is subject to change as we refine the framework based on feedback and real-world usage.

## Installation

```bash
pip install pygentic-ai
```

Or with uv:

```bash
uv add pygentic-ai
```

## Quick Start

Build your first agentic workflow in 4 steps:

### Step 1: Create Configuration

```python
from dataclasses import dataclass

@dataclass
class AppConfig:
    api_key: str
    model: str = "gpt-4o-mini"
    language: str = "english"
```

### Step 2: Build Agent Factory

Create a factory to configure your agents:

```python
from pydantic_ai import UsageLimits
from pygentic_ai import AgentManager
from pygentic_ai.engines import ReasoningAgent, GuardrailsAgent, SimpleTranslatorWorker

class AgentFactory:
    @staticmethod
    async def create_manager(config: AppConfig) -> AgentManager:
        manager = AgentManager()

        # Configure usage limits
        usage_limits = UsageLimits(output_tokens_limit=2000)

        # Register agents
        manager.register(
            "agent",
            ReasoningAgent,
            api_key=config.api_key,
            llm_model=config.model,
            language=config.language,
            usage_limits=usage_limits,
        )

        manager.register(
            "guardrails",
            GuardrailsAgent,
            api_key=config.api_key,
            llm_model=config.model,
        )

        manager.register(
            "translator",
            SimpleTranslatorWorker,
            api_key=config.api_key,
            target_language=config.language,
        )

        # Initialize all agents
        await manager.initialize()
        return manager
```

### Step 3: Set Up Workflow

Use the pre-built workflow:

```python
from pygentic_ai import user_assistant_graph

# Run workflow - manager.to_deps() automatically includes all registered agents
result = await user_assistant_graph.run(
    {"message": "Hello!"},
    manager.to_deps(chat_history=[])
)
print(result)
```

### Step 4: Put It All Together

Complete application:

```python
import asyncio
from dataclasses import dataclass
from pydantic_ai import UsageLimits
from pygentic_ai import AgentManager, user_assistant_graph
from pygentic_ai.engines import ReasoningAgent, GuardrailsAgent, SimpleTranslatorWorker

@dataclass
class AppConfig:
    api_key: str
    model: str = "gpt-4o-mini"
    language: str = "english"

class AgentFactory:
    @staticmethod
    async def create_manager(config: AppConfig) -> AgentManager:
        manager = AgentManager()
        usage_limits = UsageLimits(output_tokens_limit=2000)

        manager.register("agent", ReasoningAgent, api_key=config.api_key,
                        llm_model=config.model, usage_limits=usage_limits)
        manager.register("guardrails", GuardrailsAgent, api_key=config.api_key)
        manager.register("translator", SimpleTranslatorWorker, api_key=config.api_key)

        await manager.initialize()
        return manager

async def main():
    config = AppConfig(api_key="sk-...")
    manager = await AgentFactory.create_manager(config)

    # Use workflow
    result = await user_assistant_graph.run(
        {"message": "Hello!"},
        manager.to_deps(chat_history=[])
    )
    print(result)

    # Or use agent directly
    agent = manager.get("agent")
    result = await agent.generate_response("What's the weather?", [])
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())
```

**Complete working example**: [examples/simple-chat](examples/simple-chat)

## Advanced Usage

### Custom Agents

```python
from pygentic_ai import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            llm_vendor="openai",
            llm_model="gpt-4o",
            instructions="You are a helpful assistant.",
            **kwargs
        )
```

### Custom Workflow with Pydantic Graph

Build your own workflow by composing nodes:

```python
from pydantic_graph import Graph
from pygentic_ai.workflows.nodes import StartNode, GenerateNode, GuardrailsNode

# Define custom workflow
my_workflow = Graph(
    nodes=(StartNode, GenerateNode, GuardrailsNode),
    name="MyWorkflow"
)

# Execute with manager.to_deps()
result = await my_workflow.run(
    {"message": "Hello"},
    manager.to_deps(chat_history=[])
)
```

### Adding Custom Tools

```python
from pygentic_ai.tools import tool_manager, Toolpacks

# Get tools for your agent
tools = tool_manager.get_toolpack(AgentMode.GENERAL)

# Register agent with tools
manager.register(
    "agent",
    ReasoningAgent,
    api_key=config.api_key,
    tool_list=tools,
)
```

## API Reference

### Engines

- **BaseAgent**: Foundation for custom agents
- **ReasoningAgent**: General-purpose agent with reasoning capabilities
- **GuardrailsAgent**: Agent with content safety checks
- **GenericRouter**: Routes messages to appropriate handlers
- **SimpleTranslatorWorker**: Translates responses to different languages

### Manager

- **AgentManager**: Registry for managing multiple agents

### Workflows

- **user_assistant_graph**: Pre-built workflow with routing, generation, guardrails, and translation

### Workflow Nodes

- **StartNode**: Entry point for workflows
- **GenerateNode**: Generates responses using an agent
- **GuardrailsNode**: Applies safety checks
- **ClassifyNode**: Routes based on message classification
- **TranslateNode**: Translates output
- **RefuseNode**: Handles refused/blocked content

### State Management

- **WorkflowState**: Maintains conversation state and metadata
- **RefusalInfo**: Tracks content refusal details

### Tools

- **dateutils**: Date utility functions (get_today_date, get_current_week, get_weekday_from_date)
- **tool_registry**: ToolManager for organizing tools by agent mode

## Features

- 🚀 Built on Pydantic AI for type safety
- 🔧 Extensible agent system
- 🔄 Workflow composition with pydantic-graph
- 🛡️ Built-in guardrails
- 🌍 Multi-language support
- 🔌 MCP (Model Context Protocol) support
- 📊 Token usage tracking

## Examples

- **[Simple Chat](examples/simple-chat)**: Basic chat application showing complete workflow setup

See [examples/](examples/) for more.

## Project Structure

Recommended structure for your application:

```
your-app/
├── config.py                 # Configuration (API keys, models)
├── factories/
│   └── agent_factory.py      # Agent initialization
├── engines/                  # Custom agents (optional)
│   └── my_custom_agent.py
├── workflows/                # Custom workflows (optional)
│   └── my_workflow.py
├── nodes/                    # Custom workflow nodes (optional)
│   └── my_custom_node.py
├── tools/                    # Custom tools (optional)
│   └── my_tools.py
├── main.py                  # Application entry point
└── .env                     # Environment variables
```

### Example Custom Engine

```python
# engines/my_custom_agent.py
from pygentic_ai import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            llm_vendor="openai",
            llm_model="gpt-4o",
            instructions="You are a specialized assistant.",
            **kwargs
        )
```

### Example Custom Node

```python
# nodes/my_custom_node.py
from dataclasses import dataclass
from pydantic_graph import BaseNode, GraphRunContext
from pygentic_ai.workflows.state import WorkflowState

@dataclass
class MyCustomNode(BaseNode[WorkflowState, dict, str]):
    async def run(self, ctx: GraphRunContext[WorkflowState, dict]):
        # Your custom logic
        return NextNode()
```

### Example Custom Tools

```python
# tools/my_tools.py
def my_custom_tool(query: str) -> str:
    """Custom tool for your agent."""
    return f"Processed: {query}"

MY_TOOLS = [my_custom_tool]

# In factory:
manager.register(
    "agent",
    ReasoningAgent,
    tool_list=MY_TOOLS,
)
```

## Features

- 🚀 Built on Pydantic AI for type safety
- 🔧 Extensible agent system
- 🔄 Workflow composition with pydantic-graph
- 🛡️ Built-in guardrails
- 🌍 Multi-language support
- 🔌 MCP (Model Context Protocol) support
- 📊 Token usage tracking
