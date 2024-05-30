from enum import Enum


class RunStreamEventType0Event(str, Enum):
    THREAD_RUN_CREATED = "thread.run.created"

    def __str__(self) -> str:
        return str(self.value)
