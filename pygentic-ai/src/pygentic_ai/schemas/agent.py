"""Agent-related schemas and enums."""

from enum import Enum, StrEnum

from pydantic import BaseModel


class AgentMode(StrEnum):
    """Agent operation modes."""

    GENERAL = "general"


class TaskType(Enum):
    """Task classification types for routing."""

    conversation = 1
    refuse = 2
    translate = 3


class BaseAgentQueryRequest(BaseModel):
    """Base request model for agent queries."""

    message: str


class BaseAgentQueryResponse(BaseModel):
    """Base response model for agent queries."""

    response: str
