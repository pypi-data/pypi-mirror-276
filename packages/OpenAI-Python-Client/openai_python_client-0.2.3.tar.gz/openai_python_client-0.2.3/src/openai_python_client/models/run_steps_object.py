from enum import Enum


class RunStepsObject(str, Enum):
    THREAD_RUN_STEP = "thread.run.step"

    def __str__(self) -> str:
        return str(self.value)
