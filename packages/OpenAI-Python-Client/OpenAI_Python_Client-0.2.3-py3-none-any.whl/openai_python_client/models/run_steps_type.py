from enum import Enum


class RunStepsType(str, Enum):
    MESSAGE_CREATION = "message_creation"
    TOOL_CALLS = "tool_calls"

    def __str__(self) -> str:
        return str(self.value)
