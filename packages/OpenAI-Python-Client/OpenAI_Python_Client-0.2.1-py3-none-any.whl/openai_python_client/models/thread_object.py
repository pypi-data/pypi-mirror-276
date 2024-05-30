from enum import Enum


class ThreadObject(str, Enum):
    THREAD = "thread"

    def __str__(self) -> str:
        return str(self.value)
