from enum import Enum


class RunStreamEventType4Event(str, Enum):
    THREAD_RUN_COMPLETED = "thread.run.completed"

    def __str__(self) -> str:
        return str(self.value)
