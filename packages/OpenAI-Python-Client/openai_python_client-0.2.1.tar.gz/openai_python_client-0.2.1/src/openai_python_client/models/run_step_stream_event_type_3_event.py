from enum import Enum


class RunStepStreamEventType3Event(str, Enum):
    THREAD_RUN_STEP_COMPLETED = "thread.run.step.completed"

    def __str__(self) -> str:
        return str(self.value)
