from enum import Enum


class CreateImageRequestSize(str, Enum):
    VALUE_0 = "256x256"
    VALUE_1 = "512x512"
    VALUE_2 = "1024x1024"
    VALUE_3 = "1792x1024"
    VALUE_4 = "1024x1792"

    def __str__(self) -> str:
        return str(self.value)
