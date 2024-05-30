from enum import Enum


class RunStreamEventType5Event(str, Enum):
    THREAD_RUN_FAILED = "thread.run.failed"

    def __str__(self) -> str:
        return str(self.value)
