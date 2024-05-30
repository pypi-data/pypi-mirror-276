from enum import Enum


class ThreadTruncationControlsType(str, Enum):
    AUTO = "auto"
    LAST_MESSAGES = "last_messages"

    def __str__(self) -> str:
        return str(self.value)
