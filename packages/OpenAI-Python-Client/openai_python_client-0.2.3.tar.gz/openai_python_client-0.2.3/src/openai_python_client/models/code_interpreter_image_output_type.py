from enum import Enum


class CodeInterpreterImageOutputType(str, Enum):
    IMAGE = "image"

    def __str__(self) -> str:
        return str(self.value)
