from enum import Enum


class RunStreamEventType2Event(str, Enum):
    THREAD_RUN_IN_PROGRESS = "thread.run.in_progress"

    def __str__(self) -> str:
        return str(self.value)
