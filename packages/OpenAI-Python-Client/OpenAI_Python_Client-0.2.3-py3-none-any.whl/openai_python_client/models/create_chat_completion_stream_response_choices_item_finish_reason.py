from enum import Enum


class CreateChatCompletionStreamResponseChoicesItemFinishReason(str, Enum):
    CONTENT_FILTER = "content_filter"
    FUNCTION_CALL = "function_call"
    LENGTH = "length"
    STOP = "stop"
    TOOL_CALLS = "tool_calls"

    def __str__(self) -> str:
        return str(self.value)
