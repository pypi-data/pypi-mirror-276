from enum import Enum


class MessageStreamEventType2Event(str, Enum):
    THREAD_MESSAGE_DELTA = "thread.message.delta"

    def __str__(self) -> str:
        return str(self.value)
