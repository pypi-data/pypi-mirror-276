from enum import Enum


class RunStepStreamEventType2Event(str, Enum):
    THREAD_RUN_STEP_DELTA = "thread.run.step.delta"

    def __str__(self) -> str:
        return str(self.value)
