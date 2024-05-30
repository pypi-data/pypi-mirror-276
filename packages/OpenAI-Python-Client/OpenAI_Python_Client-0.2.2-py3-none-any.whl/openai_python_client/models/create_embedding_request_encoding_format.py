from enum import Enum


class CreateEmbeddingRequestEncodingFormat(str, Enum):
    BASE64 = "base64"
    FLOAT = "float"

    def __str__(self) -> str:
        return str(self.value)
