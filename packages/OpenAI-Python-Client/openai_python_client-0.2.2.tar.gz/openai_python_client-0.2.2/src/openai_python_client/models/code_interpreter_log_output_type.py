from enum import Enum


class CodeInterpreterLogOutputType(str, Enum):
    LOGS = "logs"

    def __str__(self) -> str:
        return str(self.value)
