from enum import Enum


class DeleteVectorStoreFileResponseObject(str, Enum):
    VECTOR_STORE_FILE_DELETED = "vector_store.file.deleted"

    def __str__(self) -> str:
        return str(self.value)
