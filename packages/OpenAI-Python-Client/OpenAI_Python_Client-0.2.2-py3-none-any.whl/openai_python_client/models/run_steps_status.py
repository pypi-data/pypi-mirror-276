from enum import Enum


class RunStepsStatus(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"

    def __str__(self) -> str:
        return str(self.value)
