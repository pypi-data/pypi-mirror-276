from enum import Enum


class RunStreamEventType7Event(str, Enum):
    THREAD_RUN_CANCELLED = "thread.run.cancelled"

    def __str__(self) -> str:
        return str(self.value)
