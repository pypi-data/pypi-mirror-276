from enum import Enum


class OpenAIFileStatus(str, Enum):
    ERROR = "error"
    PROCESSED = "processed"
    UPLOADED = "uploaded"

    def __str__(self) -> str:
        return str(self.value)
