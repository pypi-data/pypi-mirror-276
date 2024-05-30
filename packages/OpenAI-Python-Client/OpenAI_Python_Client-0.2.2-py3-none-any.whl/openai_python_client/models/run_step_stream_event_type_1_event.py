from enum import Enum


class RunStepStreamEventType1Event(str, Enum):
    THREAD_RUN_STEP_IN_PROGRESS = "thread.run.step.in_progress"

    def __str__(self) -> str:
        return str(self.value)
