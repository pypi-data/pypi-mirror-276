from io import BytesIO
from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.create_file_request_purpose import CreateFileRequestPurpose
from ..types import File

T = TypeVar("T", bound="CreateFileRequest")


@_attrs_define
class CreateFileRequest:
    """
    Attributes:
        file (File): The File object (not file name) to be uploaded.
        purpose (CreateFileRequestPurpose): The intended purpose of the uploaded file.

            Use "assistants" for [Assistants](/docs/api-reference/assistants) and [Messages](/docs/api-reference/messages),
            "batch" for [Batch API](/docs/guides/batch), and "fine-tune" for [Fine-tuning](/docs/api-reference/fine-tuning).
    """

    file: File
    purpose: CreateFileRequestPurpose

    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        purpose = self.purpose.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "file": file,
                "purpose": purpose,
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        purpose = (None, str(self.purpose.value).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "file": file,
                "purpose": purpose,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file = File(payload=BytesIO(d.pop("file")))

        purpose = CreateFileRequestPurpose(d.pop("purpose"))

        create_file_request = cls(
            file=file,
            purpose=purpose,
        )

        return create_file_request
