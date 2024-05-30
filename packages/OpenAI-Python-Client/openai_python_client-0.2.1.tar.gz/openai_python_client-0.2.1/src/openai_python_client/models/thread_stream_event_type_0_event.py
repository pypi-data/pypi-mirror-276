from enum import Enum


class ThreadStreamEventType0Event(str, Enum):
    THREAD_CREATED = "thread.created"

    def __str__(self) -> str:
        return str(self.value)
