from enum import Enum


class VectorStoreObject(str, Enum):
    VECTOR_STORE = "vector_store"

    def __str__(self) -> str:
        return str(self.value)
