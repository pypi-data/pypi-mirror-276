from enum import Enum


class CreateBatchBodyCompletionWindow(str, Enum):
    VALUE_0 = "24h"

    def __str__(self) -> str:
        return str(self.value)
