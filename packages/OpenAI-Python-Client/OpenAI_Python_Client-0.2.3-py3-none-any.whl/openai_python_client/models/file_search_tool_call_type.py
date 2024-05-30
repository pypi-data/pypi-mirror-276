from enum import Enum


class FileSearchToolCallType(str, Enum):
    FILE_SEARCH = "file_search"

    def __str__(self) -> str:
        return str(self.value)
