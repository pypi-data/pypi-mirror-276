from enum import Enum


class RunStepStreamEventType0Event(str, Enum):
    THREAD_RUN_STEP_CREATED = "thread.run.step.created"

    def __str__(self) -> str:
        return str(self.value)
