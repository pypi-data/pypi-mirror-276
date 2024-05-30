from enum import Enum


class CreateImageRequestResponseFormat(str, Enum):
    B64_JSON = "b64_json"
    URL = "url"

    def __str__(self) -> str:
        return str(self.value)
