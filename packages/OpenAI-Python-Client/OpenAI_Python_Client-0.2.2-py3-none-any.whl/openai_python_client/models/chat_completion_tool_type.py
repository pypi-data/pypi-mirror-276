from enum import Enum


class ChatCompletionToolType(str, Enum):
    FUNCTION = "function"

    def __str__(self) -> str:
        return str(self.value)
