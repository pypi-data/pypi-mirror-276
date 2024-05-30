from enum import Enum


class BatchObject(str, Enum):
    BATCH = "batch"

    def __str__(self) -> str:
        return str(self.value)
