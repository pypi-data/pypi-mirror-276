from enum import Enum


class ListVectorStoreFilesFilter(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"

    def __str__(self) -> str:
        return str(self.value)
