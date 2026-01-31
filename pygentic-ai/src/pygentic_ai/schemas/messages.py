"""Message-related schemas."""

from enum import StrEnum


class MessageRole(StrEnum):
    """Message role in conversation."""

    USER = "user"
    ASSISTANT = "assistant"
