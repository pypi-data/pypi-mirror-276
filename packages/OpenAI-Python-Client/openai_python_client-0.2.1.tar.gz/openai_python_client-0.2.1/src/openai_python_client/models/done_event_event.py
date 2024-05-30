from enum import Enum


class DoneEventEvent(str, Enum):
    DONE = "done"

    def __str__(self) -> str:
        return str(self.value)
