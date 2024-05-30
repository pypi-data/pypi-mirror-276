from enum import Enum


class TextType(str, Enum):
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
