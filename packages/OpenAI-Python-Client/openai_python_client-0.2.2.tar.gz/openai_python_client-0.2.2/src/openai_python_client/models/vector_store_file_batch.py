from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vector_store_file_batch_object import VectorStoreFileBatchObject
from ..models.vector_store_file_batch_status import VectorStoreFileBatchStatus

if TYPE_CHECKING:
    from ..models.vector_store_file_batch_file_counts import VectorStoreFileBatchFileCounts


T = TypeVar("T", bound="VectorStoreFileBatch")


@_attrs_define
class VectorStoreFileBatch:
    """A batch of files attached to a vector store.

    Attributes:
        id (str): The identifier, which can be referenced in API endpoints.
        object_ (VectorStoreFileBatchObject): The object type, which is always `vector_store.file_batch`.
        created_at (int): The Unix timestamp (in seconds) for when the vector store files batch was created.
        vector_store_id (str): The ID of the [vector store](/docs/api-reference/vector-stores/object) that the
            [File](/docs/api-reference/files) is attached to.
        status (VectorStoreFileBatchStatus): The status of the vector store files batch, which can be either
            `in_progress`, `completed`, `cancelled` or `failed`.
        file_counts (VectorStoreFileBatchFileCounts):
    """

    id: str
    object_: VectorStoreFileBatchObject
    created_at: int
    vector_store_id: str
    status: VectorStoreFileBatchStatus
    file_counts: "VectorStoreFileBatchFileCounts"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        object_ = self.object_.value

        created_at = self.created_at

        vector_store_id = self.vector_store_id

        status = self.status.value

        file_counts = self.file_counts.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "vector_store_id": vector_store_id,
                "status": status,
                "file_counts": file_counts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vector_store_file_batch_file_counts import VectorStoreFileBatchFileCounts

        d = src_dict.copy()
        id = d.pop("id")

        object_ = VectorStoreFileBatchObject(d.pop("object"))

        created_at = d.pop("created_at")

        vector_store_id = d.pop("vector_store_id")

        status = VectorStoreFileBatchStatus(d.pop("status"))

        file_counts = VectorStoreFileBatchFileCounts.from_dict(d.pop("file_counts"))

        vector_store_file_batch = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            vector_store_id=vector_store_id,
            status=status,
            file_counts=file_counts,
        )

        vector_store_file_batch.additional_properties = d
        return vector_store_file_batch

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
