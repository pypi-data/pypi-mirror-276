from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vector_store_object import VectorStoreObject
from ..models.vector_store_status import VectorStoreStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vector_store_expiration_policy import VectorStoreExpirationPolicy
    from ..models.vector_store_file_counts import VectorStoreFileCounts
    from ..models.vector_store_metadata_type_0 import VectorStoreMetadataType0


T = TypeVar("T", bound="VectorStore")


@_attrs_define
class VectorStore:
    """A vector store is a collection of processed files can be used by the `file_search` tool.

    Attributes:
        id (str): The identifier, which can be referenced in API endpoints.
        object_ (VectorStoreObject): The object type, which is always `vector_store`.
        created_at (int): The Unix timestamp (in seconds) for when the vector store was created.
        name (str): The name of the vector store.
        usage_bytes (int): The total number of bytes used by the files in the vector store.
        file_counts (VectorStoreFileCounts):
        status (VectorStoreStatus): The status of the vector store, which can be either `expired`, `in_progress`, or
            `completed`. A status of `completed` indicates that the vector store is ready for use.
        last_active_at (Union[None, int]): The Unix timestamp (in seconds) for when the vector store was last active.
        metadata (Union['VectorStoreMetadataType0', None]): Set of 16 key-value pairs that can be attached to an object.
            This can be useful for storing additional information about the object in a structured format. Keys can be a
            maximum of 64 characters long and values can be a maxium of 512 characters long.
        expires_after (Union[Unset, VectorStoreExpirationPolicy]): The expiration policy for a vector store.
        expires_at (Union[None, Unset, int]): The Unix timestamp (in seconds) for when the vector store will expire.
    """

    id: str
    object_: VectorStoreObject
    created_at: int
    name: str
    usage_bytes: int
    file_counts: "VectorStoreFileCounts"
    status: VectorStoreStatus
    last_active_at: Union[None, int]
    metadata: Union["VectorStoreMetadataType0", None]
    expires_after: Union[Unset, "VectorStoreExpirationPolicy"] = UNSET
    expires_at: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.vector_store_metadata_type_0 import VectorStoreMetadataType0

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at

        name = self.name

        usage_bytes = self.usage_bytes

        file_counts = self.file_counts.to_dict()

        status = self.status.value

        last_active_at: Union[None, int]
        last_active_at = self.last_active_at

        metadata: Union[Dict[str, Any], None]
        if isinstance(self.metadata, VectorStoreMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        expires_after: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expires_after, Unset):
            expires_after = self.expires_after.to_dict()

        expires_at: Union[None, Unset, int]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = self.expires_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "name": name,
                "usage_bytes": usage_bytes,
                "file_counts": file_counts,
                "status": status,
                "last_active_at": last_active_at,
                "metadata": metadata,
            }
        )
        if expires_after is not UNSET:
            field_dict["expires_after"] = expires_after
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vector_store_expiration_policy import VectorStoreExpirationPolicy
        from ..models.vector_store_file_counts import VectorStoreFileCounts
        from ..models.vector_store_metadata_type_0 import VectorStoreMetadataType0

        d = src_dict.copy()
        id = d.pop("id")

        object_ = VectorStoreObject(d.pop("object"))

        created_at = d.pop("created_at")

        name = d.pop("name")

        usage_bytes = d.pop("usage_bytes")

        file_counts = VectorStoreFileCounts.from_dict(d.pop("file_counts"))

        status = VectorStoreStatus(d.pop("status"))

        def _parse_last_active_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        last_active_at = _parse_last_active_at(d.pop("last_active_at"))

        def _parse_metadata(data: object) -> Union["VectorStoreMetadataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = VectorStoreMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["VectorStoreMetadataType0", None], data)

        metadata = _parse_metadata(d.pop("metadata"))

        _expires_after = d.pop("expires_after", UNSET)
        expires_after: Union[Unset, VectorStoreExpirationPolicy]
        if isinstance(_expires_after, Unset):
            expires_after = UNSET
        else:
            expires_after = VectorStoreExpirationPolicy.from_dict(_expires_after)

        def _parse_expires_at(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        vector_store = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            name=name,
            usage_bytes=usage_bytes,
            file_counts=file_counts,
            status=status,
            last_active_at=last_active_at,
            metadata=metadata,
            expires_after=expires_after,
            expires_at=expires_at,
        )

        vector_store.additional_properties = d
        return vector_store

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
