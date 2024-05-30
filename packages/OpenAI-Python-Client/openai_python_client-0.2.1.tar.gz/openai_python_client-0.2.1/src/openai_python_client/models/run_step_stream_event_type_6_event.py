from enum import Enum


class RunStepStreamEventType6Event(str, Enum):
    THREAD_RUN_STEP_EXPIRED = "thread.run.step.expired"

    def __str__(self) -> str:
        return str(self.value)
