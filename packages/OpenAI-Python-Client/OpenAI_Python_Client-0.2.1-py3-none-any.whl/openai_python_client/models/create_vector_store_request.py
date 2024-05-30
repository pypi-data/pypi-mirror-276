from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_vector_store_request_metadata_type_0 import CreateVectorStoreRequestMetadataType0
    from ..models.vector_store_expiration_policy import VectorStoreExpirationPolicy


T = TypeVar("T", bound="CreateVectorStoreRequest")


@_attrs_define
class CreateVectorStoreRequest:
    """
    Attributes:
        file_ids (Union[Unset, List[str]]): A list of [File](/docs/api-reference/files) IDs that the vector store should
            use. Useful for tools like `file_search` that can access files.
        name (Union[Unset, str]): The name of the vector store.
        expires_after (Union[Unset, VectorStoreExpirationPolicy]): The expiration policy for a vector store.
        metadata (Union['CreateVectorStoreRequestMetadataType0', None, Unset]): Set of 16 key-value pairs that can be
            attached to an object. This can be useful for storing additional information about the object in a structured
            format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
    """

    file_ids: Union[Unset, List[str]] = UNSET
    name: Union[Unset, str] = UNSET
    expires_after: Union[Unset, "VectorStoreExpirationPolicy"] = UNSET
    metadata: Union["CreateVectorStoreRequestMetadataType0", None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.create_vector_store_request_metadata_type_0 import CreateVectorStoreRequestMetadataType0

        file_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.file_ids, Unset):
            file_ids = self.file_ids

        name = self.name

        expires_after: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expires_after, Unset):
            expires_after = self.expires_after.to_dict()

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, CreateVectorStoreRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if file_ids is not UNSET:
            field_dict["file_ids"] = file_ids
        if name is not UNSET:
            field_dict["name"] = name
        if expires_after is not UNSET:
            field_dict["expires_after"] = expires_after
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_vector_store_request_metadata_type_0 import CreateVectorStoreRequestMetadataType0
        from ..models.vector_store_expiration_policy import VectorStoreExpirationPolicy

        d = src_dict.copy()
        file_ids = cast(List[str], d.pop("file_ids", UNSET))

        name = d.pop("name", UNSET)

        _expires_after = d.pop("expires_after", UNSET)
        expires_after: Union[Unset, VectorStoreExpirationPolicy]
        if isinstance(_expires_after, Unset):
            expires_after = UNSET
        else:
            expires_after = VectorStoreExpirationPolicy.from_dict(_expires_after)

        def _parse_metadata(data: object) -> Union["CreateVectorStoreRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = CreateVectorStoreRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateVectorStoreRequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        create_vector_store_request = cls(
            file_ids=file_ids,
            name=name,
            expires_after=expires_after,
            metadata=metadata,
        )

        return create_vector_store_request
