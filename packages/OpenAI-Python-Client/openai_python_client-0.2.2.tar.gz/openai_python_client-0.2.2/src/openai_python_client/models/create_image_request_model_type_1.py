from enum import Enum


class CreateImageRequestModelType1(str, Enum):
    DALL_E_2 = "dall-e-2"
    DALL_E_3 = "dall-e-3"

    def __str__(self) -> str:
        return str(self.value)
