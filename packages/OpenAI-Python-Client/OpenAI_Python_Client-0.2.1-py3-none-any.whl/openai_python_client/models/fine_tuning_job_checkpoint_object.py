from enum import Enum


class FineTuningJobCheckpointObject(str, Enum):
    FINE_TUNING_JOB_CHECKPOINT = "fine_tuning.job.checkpoint"

    def __str__(self) -> str:
        return str(self.value)
