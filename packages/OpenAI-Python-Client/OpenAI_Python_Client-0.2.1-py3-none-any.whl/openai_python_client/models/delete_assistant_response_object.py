from enum import Enum


class DeleteAssistantResponseObject(str, Enum):
    ASSISTANT_DELETED = "assistant.deleted"

    def __str__(self) -> str:
        return str(self.value)
