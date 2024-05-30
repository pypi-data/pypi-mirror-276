from enum import Enum


class SystemMessageRole(str, Enum):
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
