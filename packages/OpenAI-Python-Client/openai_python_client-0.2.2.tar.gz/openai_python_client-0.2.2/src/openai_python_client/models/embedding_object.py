from enum import Enum


class EmbeddingObject(str, Enum):
    EMBEDDING = "embedding"

    def __str__(self) -> str:
        return str(self.value)
