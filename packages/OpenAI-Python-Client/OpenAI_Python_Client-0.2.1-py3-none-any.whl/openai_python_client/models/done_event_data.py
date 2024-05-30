from enum import Enum


class DoneEventData(str, Enum):
    VALUE_0 = "[DONE]"

    def __str__(self) -> str:
        return str(self.value)
