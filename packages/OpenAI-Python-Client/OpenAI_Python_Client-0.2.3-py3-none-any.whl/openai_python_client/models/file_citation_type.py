from enum import Enum


class FileCitationType(str, Enum):
    FILE_CITATION = "file_citation"

    def __str__(self) -> str:
        return str(self.value)
