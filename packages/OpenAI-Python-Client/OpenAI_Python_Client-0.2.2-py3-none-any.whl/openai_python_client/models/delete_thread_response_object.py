from enum import Enum


class DeleteThreadResponseObject(str, Enum):
    THREAD_DELETED = "thread.deleted"

    def __str__(self) -> str:
        return str(self.value)
