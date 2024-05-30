from enum import Enum


class AssistantsNamedToolChoiceType(str, Enum):
    CODE_INTERPRETER = "code_interpreter"
    FILE_SEARCH = "file_search"
    FUNCTION = "function"

    def __str__(self) -> str:
        return str(self.value)
