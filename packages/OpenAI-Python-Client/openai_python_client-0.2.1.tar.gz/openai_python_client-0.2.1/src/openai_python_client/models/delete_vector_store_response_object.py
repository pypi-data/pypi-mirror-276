from enum import Enum


class DeleteVectorStoreResponseObject(str, Enum):
    VECTOR_STORE_DELETED = "vector_store.deleted"

    def __str__(self) -> str:
        return str(self.value)
