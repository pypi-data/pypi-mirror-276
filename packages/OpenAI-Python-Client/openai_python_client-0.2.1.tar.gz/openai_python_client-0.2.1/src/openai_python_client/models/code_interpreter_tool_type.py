from enum import Enum


class CodeInterpreterToolType(str, Enum):
    CODE_INTERPRETER = "code_interpreter"

    def __str__(self) -> str:
        return str(self.value)
