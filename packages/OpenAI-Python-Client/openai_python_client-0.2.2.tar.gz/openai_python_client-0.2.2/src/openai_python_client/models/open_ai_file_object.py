from enum import Enum


class OpenAIFileObject(str, Enum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
