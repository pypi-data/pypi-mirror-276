from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modify_run_request_metadata_type_0 import ModifyRunRequestMetadataType0


T = TypeVar("T", bound="ModifyRunRequest")


@_attrs_define
class ModifyRunRequest:
    """
    Attributes:
        metadata (Union['ModifyRunRequestMetadataType0', None, Unset]): Set of 16 key-value pairs that can be attached
            to an object. This can be useful for storing additional information about the object in a structured format.
            Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
    """

    metadata: Union["ModifyRunRequestMetadataType0", None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.modify_run_request_metadata_type_0 import ModifyRunRequestMetadataType0

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ModifyRunRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.modify_run_request_metadata_type_0 import ModifyRunRequestMetadataType0

        d = src_dict.copy()

        def _parse_metadata(data: object) -> Union["ModifyRunRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ModifyRunRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ModifyRunRequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        modify_run_request = cls(
            metadata=metadata,
        )

        return modify_run_request
