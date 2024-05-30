from enum import Enum


class DeleteMessageResponseObject(str, Enum):
    THREAD_MESSAGE_DELETED = "thread.message.deleted"

    def __str__(self) -> str:
        return str(self.value)
