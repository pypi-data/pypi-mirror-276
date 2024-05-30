from enum import Enum


class CreateSpeechRequestModelType1(str, Enum):
    TTS_1 = "tts-1"
    TTS_1_HD = "tts-1-hd"

    def __str__(self) -> str:
        return str(self.value)
