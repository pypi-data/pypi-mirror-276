from enum import Enum


class VectorStoreStatus(str, Enum):
    COMPLETED = "completed"
    EXPIRED = "expired"
    IN_PROGRESS = "in_progress"

    def __str__(self) -> str:
        return str(self.value)
