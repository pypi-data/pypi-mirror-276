from enum import Enum


class FineTuningJobEventObject(str, Enum):
    FINE_TUNING_JOB_EVENT = "fine_tuning.job.event"

    def __str__(self) -> str:
        return str(self.value)
