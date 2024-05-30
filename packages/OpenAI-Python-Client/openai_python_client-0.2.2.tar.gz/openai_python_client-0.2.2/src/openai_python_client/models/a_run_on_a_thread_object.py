from enum import Enum


class ARunOnAThreadObject(str, Enum):
    THREAD_RUN = "thread.run"

    def __str__(self) -> str:
        return str(self.value)
