from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="CreateVectorStoreFileBatchRequest")


@_attrs_define
class CreateVectorStoreFileBatchRequest:
    """
    Attributes:
        file_ids (List[str]): A list of [File](/docs/api-reference/files) IDs that the vector store should use. Useful
            for tools like `file_search` that can access files.
    """

    file_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        file_ids = self.file_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "file_ids": file_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_ids = cast(List[str], d.pop("file_ids"))

        create_vector_store_file_batch_request = cls(
            file_ids=file_ids,
        )

        return create_vector_store_file_batch_request
