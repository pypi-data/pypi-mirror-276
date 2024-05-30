from enum import Enum


class CreateImageRequestQuality(str, Enum):
    HD = "hd"
    STANDARD = "standard"

    def __str__(self) -> str:
        return str(self.value)
