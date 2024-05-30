from enum import Enum


class ARunOnAThreadStatus(str, Enum):
    CANCELLED = "cancelled"
    CANCELLING = "cancelling"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    QUEUED = "queued"
    REQUIRES_ACTION = "requires_action"

    def __str__(self) -> str:
        return str(self.value)
