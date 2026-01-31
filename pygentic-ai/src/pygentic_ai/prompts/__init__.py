"""Agent prompts and instructions."""

from pygentic_ai.prompts.agent_prompts import (
    TEXT_AGENT_PRIMING,
    TEXT_AGENT_RULES,
    TEXT_REACTAGENT_GUIDANCE,
    get_general_instructions,
    get_instructions_for_mode,
    get_language_instruction,
)
from pygentic_ai.prompts.worker_prompts import (
    TEXT_GUARDRAILS_INSTRUCTIONS,
    TEXT_ROUTER_INSTRUCTIONS,
    TEXT_TRANSLATOR_INSTRUCTIONS,
    get_guardrails_instructions,
    get_router_instructions,
    get_translator_instructions,
)

__all__ = [
    # Agent prompts
    "TEXT_AGENT_PRIMING",
    "TEXT_AGENT_RULES",
    "TEXT_REACTAGENT_GUIDANCE",
    "get_general_instructions",
    "get_instructions_for_mode",
    "get_language_instruction",
    # Worker prompts
    "TEXT_GUARDRAILS_INSTRUCTIONS",
    "TEXT_ROUTER_INSTRUCTIONS",
    "TEXT_TRANSLATOR_INSTRUCTIONS",
    "get_guardrails_instructions",
    "get_router_instructions",
    "get_translator_instructions",
]
