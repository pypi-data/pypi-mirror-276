from enum import Enum


class CreateSpeechRequestVoice(str, Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    NOVA = "nova"
    ONYX = "onyx"
    SHIMMER = "shimmer"

    def __str__(self) -> str:
        return str(self.value)
