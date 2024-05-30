from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.a_run_on_a_thread_incomplete_details_type_0_reason import ARunOnAThreadIncompleteDetailsType0Reason
from ..types import UNSET, Unset

T = TypeVar("T", bound="ARunOnAThreadIncompleteDetailsType0")


@_attrs_define
class ARunOnAThreadIncompleteDetailsType0:
    """Details on why the run is incomplete. Will be `null` if the run is not incomplete.

    Attributes:
        reason (Union[Unset, ARunOnAThreadIncompleteDetailsType0Reason]): The reason why the run is incomplete. This
            will point to which specific token limit was reached over the course of the run.
    """

    reason: Union[Unset, ARunOnAThreadIncompleteDetailsType0Reason] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, ARunOnAThreadIncompleteDetailsType0Reason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = ARunOnAThreadIncompleteDetailsType0Reason(_reason)

        a_run_on_a_thread_incomplete_details_type_0 = cls(
            reason=reason,
        )

        a_run_on_a_thread_incomplete_details_type_0.additional_properties = d
        return a_run_on_a_thread_incomplete_details_type_0

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
