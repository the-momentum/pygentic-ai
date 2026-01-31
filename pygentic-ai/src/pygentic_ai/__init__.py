"""
pygentic-ai: A meta-framework for building agentic workflows with Pydantic AI.

This package provides building blocks for creating custom AI agent workflows:
- BaseAgent: Base class for creating custom agents
- AgentManager: Registry for managing agents and workers
- WorkflowState: State management for workflows
- Workflow Nodes: Reusable workflow components
- Tools: Utility functions for agents
"""

from pygentic_ai.engines.base import BaseAgent, BaseAgentDeps
from pygentic_ai.manager import AgentManager
from pygentic_ai.schemas import AgentMode, TaskType
from pygentic_ai.workflows.agent_workflow import user_assistant_graph
from pygentic_ai.workflows.state import RefusalInfo, WorkflowState

__all__ = [
    # Core classes
    "BaseAgent",
    "BaseAgentDeps",
    "AgentManager",
    # Workflow
    "user_assistant_graph",
    # State
    "WorkflowState",
    "RefusalInfo",
    # Enums
    "AgentMode",
    "TaskType",
]


def __getattr__(name: str) -> str:
    """Lazy load version from package metadata."""
    if name == "__version__":
        from importlib.metadata import version

        return version("pygentic-ai")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
