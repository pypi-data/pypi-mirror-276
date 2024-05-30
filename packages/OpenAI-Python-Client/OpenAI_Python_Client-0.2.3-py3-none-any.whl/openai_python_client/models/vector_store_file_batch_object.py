from enum import Enum


class VectorStoreFileBatchObject(str, Enum):
    VECTOR_STORE_FILES_BATCH = "vector_store.files_batch"

    def __str__(self) -> str:
        return str(self.value)
