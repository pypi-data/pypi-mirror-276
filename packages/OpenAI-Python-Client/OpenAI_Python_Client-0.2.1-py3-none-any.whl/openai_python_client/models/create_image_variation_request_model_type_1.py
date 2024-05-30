from enum import Enum


class CreateImageVariationRequestModelType1(str, Enum):
    DALL_E_2 = "dall-e-2"

    def __str__(self) -> str:
        return str(self.value)
