"""Tool registry for managing agent toolpacks."""

from enum import Enum
from typing import Any, Callable

from pygentic_ai.schemas import AgentMode
from pygentic_ai.tools.dateutils import DATEUTILS_TOOLS


class Toolpacks(Enum):
    """Available toolpacks for agents."""

    GENERAL = "general"
    UTILS = "dateutils"


class ToolManager:
    """Manager for organizing tools by agent mode."""

    toolpacks: dict[Toolpacks, list[Callable[..., Any]]] = {
        Toolpacks.GENERAL: [],
        Toolpacks.UTILS: DATEUTILS_TOOLS,
    }

    mapping: dict[AgentMode, list[Toolpacks]] = {
        AgentMode.GENERAL: [Toolpacks.GENERAL, Toolpacks.UTILS],
    }

    def get_toolpack(self, agent_mode: AgentMode) -> list[Callable[..., Any]]:
        """Get tools for a specific agent mode."""
        tool_list = []
        required_toolpacks = self.mapping.get(agent_mode, [])

        for toolpack in required_toolpacks:
            tools = self.toolpacks.get(toolpack, [])
            tool_list.extend(tools)

        return tool_list


tool_manager = ToolManager()
