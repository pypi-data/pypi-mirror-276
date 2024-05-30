from enum import Enum


class CreateEmbeddingRequestModelType1(str, Enum):
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"

    def __str__(self) -> str:
        return str(self.value)
