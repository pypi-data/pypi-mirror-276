from enum import Enum


class CreateBatchBodyEndpoint(str, Enum):
    VALUE_0 = "/v1/chat/completions"
    VALUE_1 = "/v1/embeddings"

    def __str__(self) -> str:
        return str(self.value)
