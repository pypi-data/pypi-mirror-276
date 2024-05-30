from enum import Enum


class RunStreamEventType3Event(str, Enum):
    THREAD_RUN_REQUIRES_ACTION = "thread.run.requires_action"

    def __str__(self) -> str:
        return str(self.value)
