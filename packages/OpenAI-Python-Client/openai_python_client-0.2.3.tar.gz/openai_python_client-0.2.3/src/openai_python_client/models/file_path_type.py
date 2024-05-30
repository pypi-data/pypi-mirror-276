from enum import Enum


class FilePathType(str, Enum):
    FILE_PATH = "file_path"

    def __str__(self) -> str:
        return str(self.value)
