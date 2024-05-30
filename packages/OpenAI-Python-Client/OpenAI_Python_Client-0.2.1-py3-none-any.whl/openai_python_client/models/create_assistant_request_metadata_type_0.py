from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateAssistantRequestMetadataType0")


@_attrs_define
class CreateAssistantRequestMetadataType0:
    """Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information
    about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maxium of
    512 characters long.

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        create_assistant_request_metadata_type_0 = cls()

        create_assistant_request_metadata_type_0.additional_properties = d
        return create_assistant_request_metadata_type_0

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
