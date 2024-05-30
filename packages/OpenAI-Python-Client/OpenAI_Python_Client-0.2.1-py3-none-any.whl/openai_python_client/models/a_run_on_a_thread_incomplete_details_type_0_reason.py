from enum import Enum


class ARunOnAThreadIncompleteDetailsType0Reason(str, Enum):
    MAX_COMPLETION_TOKENS = "max_completion_tokens"
    MAX_PROMPT_TOKENS = "max_prompt_tokens"

    def __str__(self) -> str:
        return str(self.value)
