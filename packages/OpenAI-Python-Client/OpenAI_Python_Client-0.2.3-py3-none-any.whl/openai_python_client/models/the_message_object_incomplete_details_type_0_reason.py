from enum import Enum


class TheMessageObjectIncompleteDetailsType0Reason(str, Enum):
    CONTENT_FILTER = "content_filter"
    MAX_TOKENS = "max_tokens"
    RUN_CANCELLED = "run_cancelled"
    RUN_EXPIRED = "run_expired"
    RUN_FAILED = "run_failed"

    def __str__(self) -> str:
        return str(self.value)
