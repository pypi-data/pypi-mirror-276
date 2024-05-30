from enum import Enum


class BatchStatus(str, Enum):
    CANCELLED = "cancelled"
    CANCELLING = "cancelling"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"
    FINALIZING = "finalizing"
    IN_PROGRESS = "in_progress"
    VALIDATING = "validating"

    def __str__(self) -> str:
        return str(self.value)
