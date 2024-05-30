from enum import Enum


class CreateTranslationRequestModelType1(str, Enum):
    WHISPER_1 = "whisper-1"

    def __str__(self) -> str:
        return str(self.value)
