from enum import Enum


class VectorStoreExpirationPolicyAnchor(str, Enum):
    LAST_ACTIVE_AT = "last_active_at"

    def __str__(self) -> str:
        return str(self.value)
