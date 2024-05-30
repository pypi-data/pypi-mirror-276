from enum import Enum


class MessageStreamEventType0Event(str, Enum):
    THREAD_MESSAGE_CREATED = "thread.message.created"

    def __str__(self) -> str:
        return str(self.value)
