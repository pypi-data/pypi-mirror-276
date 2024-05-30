from enum import Enum


class CreateCompletionResponseObject(str, Enum):
    TEXT_COMPLETION = "text_completion"

    def __str__(self) -> str:
        return str(self.value)
