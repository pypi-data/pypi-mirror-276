from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.the_message_object_incomplete_details_type_0_reason import TheMessageObjectIncompleteDetailsType0Reason

T = TypeVar("T", bound="TheMessageObjectIncompleteDetailsType0")


@_attrs_define
class TheMessageObjectIncompleteDetailsType0:
    """On an incomplete message, details about why the message is incomplete.

    Attributes:
        reason (TheMessageObjectIncompleteDetailsType0Reason): The reason the message is incomplete.
    """

    reason: TheMessageObjectIncompleteDetailsType0Reason
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reason = TheMessageObjectIncompleteDetailsType0Reason(d.pop("reason"))

        the_message_object_incomplete_details_type_0 = cls(
            reason=reason,
        )

        the_message_object_incomplete_details_type_0.additional_properties = d
        return the_message_object_incomplete_details_type_0

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
