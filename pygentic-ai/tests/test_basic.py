"""Basic tests for pygentic-ai imports and version."""

import pytest


def test_imports() -> None:
    """Test that main imports work."""
    from pygentic_ai import (
        AgentManager,
        AgentMode,
        BaseAgent,
        BaseAgentDeps,
        RefusalInfo,
        TaskType,
        WorkflowState,
    )

    assert BaseAgent is not None
    assert BaseAgentDeps is not None
    assert AgentManager is not None
    assert WorkflowState is not None
    assert RefusalInfo is not None
    assert AgentMode is not None
    assert TaskType is not None


def test_engines_imports() -> None:
    """Test that engines module imports work."""
    from pygentic_ai.engines import (
        BaseAgent,
        GenericRouter,
        GuardrailsAgent,
        ReasoningAgent,
        SimpleTranslatorWorker,
    )

    assert BaseAgent is not None
    assert GenericRouter is not None
    assert SimpleTranslatorWorker is not None
    assert GuardrailsAgent is not None
    assert ReasoningAgent is not None


def test_workflow_nodes_imports() -> None:
    """Test that workflow nodes imports work."""
    from pygentic_ai.workflows.nodes import (
        ClassifyNode,
        GenerateNode,
        GuardrailsNode,
        RefuseNode,
        StartNode,
        TranslateNode,
    )

    assert StartNode is not None
    assert ClassifyNode is not None
    assert GenerateNode is not None
    assert GuardrailsNode is not None
    assert RefuseNode is not None
    assert TranslateNode is not None


def test_workflow_state() -> None:
    """Test WorkflowState functionality."""
    from pygentic_ai import TaskType, WorkflowState

    state = WorkflowState()
    assert state.current_message == ""
    assert state.task_type is None
    assert state.generated_response == ""
    assert state.refusal_info is None

    state.current_message = "Hello"
    state.task_type = TaskType.conversation
    assert state.current_message == "Hello"
    assert state.task_type == TaskType.conversation


def test_workflow_state_refusal() -> None:
    """Test WorkflowState refusal functionality."""
    from pygentic_ai import WorkflowState

    state = WorkflowState()
    state.set_refusal("Bad message", "Policy violation")

    assert state.refusal_info is not None
    assert state.refusal_info.refusal_reason == "Policy violation"


def test_agent_manager() -> None:
    """Test AgentManager basic functionality."""
    from pygentic_ai import AgentManager

    manager = AgentManager()

    assert manager.list_agents() == []
    assert not manager.has("test")

    # Test registration
    class DummyAgent:
        pass

    manager.register("dummy", DummyAgent)
    assert manager.has("dummy")
    assert "dummy" in manager.list_agents()


@pytest.mark.asyncio
async def test_agent_manager_initialize() -> None:
    """Test AgentManager initialization."""
    from pygentic_ai import AgentManager

    class DummyAgent:
        def __init__(self, value: str = "default"):
            self.value = value

    manager = AgentManager()
    manager.register("dummy", DummyAgent, value="custom")

    await manager.initialize()

    agent = manager.get("dummy")
    assert agent.value == "custom"


def test_task_type_values() -> None:
    """Test TaskType enum values."""
    from pygentic_ai import TaskType

    assert TaskType.conversation.value == 1
    assert TaskType.refuse.value == 2
    assert TaskType.translate.value == 3


def test_agent_mode() -> None:
    """Test AgentMode enum."""
    from pygentic_ai import AgentMode

    assert AgentMode.GENERAL == "general"
