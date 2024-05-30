from enum import Enum


class FineTuningJobObject(str, Enum):
    FINE_TUNING_JOB = "fine_tuning.job"

    def __str__(self) -> str:
        return str(self.value)
