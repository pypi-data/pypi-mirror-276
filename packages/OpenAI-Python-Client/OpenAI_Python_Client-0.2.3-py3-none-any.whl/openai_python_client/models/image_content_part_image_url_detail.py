from enum import Enum


class ImageContentPartImageUrlDetail(str, Enum):
    AUTO = "auto"
    HIGH = "high"
    LOW = "low"

    def __str__(self) -> str:
        return str(self.value)
