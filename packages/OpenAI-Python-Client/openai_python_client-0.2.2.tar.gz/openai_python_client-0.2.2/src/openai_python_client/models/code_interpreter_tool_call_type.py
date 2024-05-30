from enum import Enum


class CodeInterpreterToolCallType(str, Enum):
    CODE_INTERPRETER = "code_interpreter"

    def __str__(self) -> str:
        return str(self.value)
