from enum import Enum


class CreateTranscriptionRequestTimestampGranularitiesItem(str, Enum):
    SEGMENT = "segment"
    WORD = "word"

    def __str__(self) -> str:
        return str(self.value)
