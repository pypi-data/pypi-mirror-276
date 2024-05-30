from enum import Enum


class CreateChatCompletionFunctionResponseChoicesItemFinishReason(str, Enum):
    CONTENT_FILTER = "content_filter"
    FUNCTION_CALL = "function_call"
    LENGTH = "length"
    STOP = "stop"

    def __str__(self) -> str:
        return str(self.value)
