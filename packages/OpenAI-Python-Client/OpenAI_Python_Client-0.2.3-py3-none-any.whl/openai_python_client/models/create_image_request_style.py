from enum import Enum


class CreateImageRequestStyle(str, Enum):
    NATURAL = "natural"
    VIVID = "vivid"

    def __str__(self) -> str:
        return str(self.value)
