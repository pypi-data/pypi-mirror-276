from enum import Enum


class RunStreamEventType8Event(str, Enum):
    THREAD_RUN_EXPIRED = "thread.run.expired"

    def __str__(self) -> str:
        return str(self.value)
