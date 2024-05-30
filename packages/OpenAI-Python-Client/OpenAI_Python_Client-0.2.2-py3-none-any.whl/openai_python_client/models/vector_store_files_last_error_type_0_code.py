from enum import Enum


class VectorStoreFilesLastErrorType0Code(str, Enum):
    FILE_NOT_FOUND = "file_not_found"
    INTERNAL_ERROR = "internal_error"
    PARSING_ERROR = "parsing_error"
    UNHANDLED_MIME_TYPE = "unhandled_mime_type"

    def __str__(self) -> str:
        return str(self.value)
