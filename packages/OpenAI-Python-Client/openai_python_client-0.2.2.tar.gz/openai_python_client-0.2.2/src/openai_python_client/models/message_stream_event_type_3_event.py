from enum import Enum


class MessageStreamEventType3Event(str, Enum):
    THREAD_MESSAGE_COMPLETED = "thread.message.completed"

    def __str__(self) -> str:
        return str(self.value)
