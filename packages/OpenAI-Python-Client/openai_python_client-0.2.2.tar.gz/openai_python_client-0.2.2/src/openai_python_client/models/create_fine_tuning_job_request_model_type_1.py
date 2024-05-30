from enum import Enum


class CreateFineTuningJobRequestModelType1(str, Enum):
    BABBAGE_002 = "babbage-002"
    DAVINCI_002 = "davinci-002"
    GPT_3_5_TURBO = "gpt-3.5-turbo"

    def __str__(self) -> str:
        return str(self.value)
