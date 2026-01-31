"""Workflow state classes for managing workflow execution."""

from dataclasses import dataclass

from pygentic_ai.schemas.agent import TaskType


@dataclass
class RefusalInfo:
    """Information about why a request was refused."""

    refusal_reason: str


@dataclass
class ErrorState:
    """State for error tracking in workflows."""

    error_step: str
    error: Exception
    error_msg: str | None


@dataclass
class TextEvaluationState:
    """State for text evaluation workflows."""

    message: str


@dataclass
class TextGenerationState:
    """State for text generation workflows."""

    message: str
    task_type: TaskType


@dataclass
class GuardrailsState:
    """State for guardrails processing."""

    message: str
    task_type: TaskType


@dataclass
class TextRefusalState:
    """State for refusal handling."""

    message: str
    refusal_reason: str


@dataclass
class WorkflowState:
    """Main workflow state container.

    This class maintains the state throughout a workflow execution,
    including the current message, task classification, generated response,
    and any refusal information.

    Attributes:
        current_message: The current user message being processed
        task_type: The classified task type (conversation, refuse, translate)
        generated_response: The generated response from the agent
        refusal_info: Information about refusal if applicable

    Example:
        ```python
        from pygentic_ai.workflows import WorkflowState

        state = WorkflowState()
        state.current_message = "Hello, how are you?"
        state.task_type = TaskType.conversation
        ```
    """

    current_message: str = ""
    task_type: TaskType | None = None
    generated_response: str = ""
    refusal_info: RefusalInfo | None = None

    def set_refusal(self, message: str, reason: str) -> None:
        """Set refusal information.

        Args:
            message: The original message that was refused
            reason: The reason for refusal
        """
        self.refusal_info = RefusalInfo(refusal_reason=reason)
