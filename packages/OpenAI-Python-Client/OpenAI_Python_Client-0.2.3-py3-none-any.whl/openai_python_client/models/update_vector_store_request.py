from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_vector_store_request_metadata_type_0 import UpdateVectorStoreRequestMetadataType0
    from ..models.vector_store_expiration_policy import VectorStoreExpirationPolicy


T = TypeVar("T", bound="UpdateVectorStoreRequest")


@_attrs_define
class UpdateVectorStoreRequest:
    """
    Attributes:
        name (Union[None, Unset, str]): The name of the vector store.
        expires_after (Union[Unset, VectorStoreExpirationPolicy]): The expiration policy for a vector store.
        metadata (Union['UpdateVectorStoreRequestMetadataType0', None, Unset]): Set of 16 key-value pairs that can be
            attached to an object. This can be useful for storing additional information about the object in a structured
            format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
    """

    name: Union[None, Unset, str] = UNSET
    expires_after: Union[Unset, "VectorStoreExpirationPolicy"] = UNSET
    metadata: Union["UpdateVectorStoreRequestMetadataType0", None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.update_vector_store_request_metadata_type_0 import UpdateVectorStoreRequestMetadataType0

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        expires_after: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expires_after, Unset):
            expires_after = self.expires_after.to_dict()

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, UpdateVectorStoreRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if expires_after is not UNSET:
            field_dict["expires_after"] = expires_after
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_vector_store_request_metadata_type_0 import UpdateVectorStoreRequestMetadataType0
        from ..models.vector_store_expiration_policy import VectorStoreExpirationPolicy

        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        _expires_after = d.pop("expires_after", UNSET)
        expires_after: Union[Unset, VectorStoreExpirationPolicy]
        if isinstance(_expires_after, Unset):
            expires_after = UNSET
        else:
            expires_after = VectorStoreExpirationPolicy.from_dict(_expires_after)

        def _parse_metadata(data: object) -> Union["UpdateVectorStoreRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = UpdateVectorStoreRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["UpdateVectorStoreRequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        update_vector_store_request = cls(
            name=name,
            expires_after=expires_after,
            metadata=metadata,
        )

        return update_vector_store_request
