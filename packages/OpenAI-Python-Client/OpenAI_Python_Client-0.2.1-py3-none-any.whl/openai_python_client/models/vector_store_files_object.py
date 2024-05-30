from enum import Enum


class VectorStoreFilesObject(str, Enum):
    VECTOR_STORE_FILE = "vector_store.file"

    def __str__(self) -> str:
        return str(self.value)
