from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CreateVectorStoreFileRequest")


@_attrs_define
class CreateVectorStoreFileRequest:
    """
    Attributes:
        file_id (str): A [File](/docs/api-reference/files) ID that the vector store should use. Useful for tools like
            `file_search` that can access files.
    """

    file_id: str

    def to_dict(self) -> Dict[str, Any]:
        file_id = self.file_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "file_id": file_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_id = d.pop("file_id")

        create_vector_store_file_request = cls(
            file_id=file_id,
        )

        return create_vector_store_file_request
