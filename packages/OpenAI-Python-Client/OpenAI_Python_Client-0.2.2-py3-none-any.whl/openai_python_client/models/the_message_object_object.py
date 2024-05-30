from enum import Enum


class TheMessageObjectObject(str, Enum):
    THREAD_MESSAGE = "thread.message"

    def __str__(self) -> str:
        return str(self.value)
