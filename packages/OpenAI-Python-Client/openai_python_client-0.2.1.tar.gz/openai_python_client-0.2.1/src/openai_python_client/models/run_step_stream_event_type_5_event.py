from enum import Enum


class RunStepStreamEventType5Event(str, Enum):
    THREAD_RUN_STEP_CANCELLED = "thread.run.step.cancelled"

    def __str__(self) -> str:
        return str(self.value)
