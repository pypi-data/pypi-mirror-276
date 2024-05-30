from enum import Enum


class MessageStreamEventType4Event(str, Enum):
    THREAD_MESSAGE_INCOMPLETE = "thread.message.incomplete"

    def __str__(self) -> str:
        return str(self.value)
