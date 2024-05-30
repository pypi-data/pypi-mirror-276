from enum import Enum


class CreateChatCompletionFunctionResponseObject(str, Enum):
    CHAT_COMPLETION = "chat.completion"

    def __str__(self) -> str:
        return str(self.value)
