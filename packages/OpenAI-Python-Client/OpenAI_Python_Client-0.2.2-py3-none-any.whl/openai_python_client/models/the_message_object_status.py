from enum import Enum


class TheMessageObjectStatus(str, Enum):
    COMPLETED = "completed"
    INCOMPLETE = "incomplete"
    IN_PROGRESS = "in_progress"

    def __str__(self) -> str:
        return str(self.value)
