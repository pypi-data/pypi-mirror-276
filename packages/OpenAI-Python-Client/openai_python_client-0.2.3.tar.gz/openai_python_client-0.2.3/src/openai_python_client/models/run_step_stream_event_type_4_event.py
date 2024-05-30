from enum import Enum


class RunStepStreamEventType4Event(str, Enum):
    THREAD_RUN_STEP_FAILED = "thread.run.step.failed"

    def __str__(self) -> str:
        return str(self.value)
