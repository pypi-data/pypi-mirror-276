from enum import Enum


class RunStreamEventType1Event(str, Enum):
    THREAD_RUN_QUEUED = "thread.run.queued"

    def __str__(self) -> str:
        return str(self.value)
