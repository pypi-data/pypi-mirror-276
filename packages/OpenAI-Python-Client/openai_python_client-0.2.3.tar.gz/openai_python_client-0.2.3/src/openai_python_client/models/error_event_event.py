from enum import Enum


class ErrorEventEvent(str, Enum):
    ERROR = "error"

    def __str__(self) -> str:
        return str(self.value)
