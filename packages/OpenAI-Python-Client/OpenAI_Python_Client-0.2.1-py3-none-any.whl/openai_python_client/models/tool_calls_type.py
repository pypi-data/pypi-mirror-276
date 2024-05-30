from enum import Enum


class ToolCallsType(str, Enum):
    TOOL_CALLS = "tool_calls"

    def __str__(self) -> str:
        return str(self.value)
