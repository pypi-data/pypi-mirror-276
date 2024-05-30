from enum import Enum


class ARunOnAThreadLastErrorType0Code(str, Enum):
    INVALID_PROMPT = "invalid_prompt"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SERVER_ERROR = "server_error"

    def __str__(self) -> str:
        return str(self.value)
