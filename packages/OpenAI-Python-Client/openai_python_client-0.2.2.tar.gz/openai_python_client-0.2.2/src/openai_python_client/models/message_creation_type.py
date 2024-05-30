from enum import Enum


class MessageCreationType(str, Enum):
    MESSAGE_CREATION = "message_creation"

    def __str__(self) -> str:
        return str(self.value)
