from enum import Enum


class RunStepsLastErrorType0Code(str, Enum):
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SERVER_ERROR = "server_error"

    def __str__(self) -> str:
        return str(self.value)
