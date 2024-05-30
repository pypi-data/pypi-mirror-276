from enum import Enum


class MessageStreamEventType1Event(str, Enum):
    THREAD_MESSAGE_IN_PROGRESS = "thread.message.in_progress"

    def __str__(self) -> str:
        return str(self.value)
