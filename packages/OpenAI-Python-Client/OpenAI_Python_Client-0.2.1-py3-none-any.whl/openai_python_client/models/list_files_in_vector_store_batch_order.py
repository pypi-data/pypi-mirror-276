from enum import Enum


class ListFilesInVectorStoreBatchOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)
