from enum import Enum


class RunStreamEventType6Event(str, Enum):
    THREAD_RUN_CANCELLING = "thread.run.cancelling"

    def __str__(self) -> str:
        return str(self.value)
