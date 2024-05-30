from enum import Enum


class FineTuningJobStatus(str, Enum):
    CANCELLED = "cancelled"
    FAILED = "failed"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    VALIDATING_FILES = "validating_files"

    def __str__(self) -> str:
        return str(self.value)
