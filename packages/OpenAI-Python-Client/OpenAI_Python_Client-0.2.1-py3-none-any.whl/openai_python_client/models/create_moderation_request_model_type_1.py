from enum import Enum


class CreateModerationRequestModelType1(str, Enum):
    TEXT_MODERATION_LATEST = "text-moderation-latest"
    TEXT_MODERATION_STABLE = "text-moderation-stable"

    def __str__(self) -> str:
        return str(self.value)
