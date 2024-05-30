from enum import Enum


class CreateCompletionResponseChoicesItemFinishReason(str, Enum):
    CONTENT_FILTER = "content_filter"
    LENGTH = "length"
    STOP = "stop"

    def __str__(self) -> str:
        return str(self.value)
