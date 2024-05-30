from enum import Enum


class FunctionToolCallType(str, Enum):
    FUNCTION = "function"

    def __str__(self) -> str:
        return str(self.value)
