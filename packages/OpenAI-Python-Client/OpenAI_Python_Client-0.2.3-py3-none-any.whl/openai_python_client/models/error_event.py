from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_event_event import ErrorEventEvent

if TYPE_CHECKING:
    from ..models.error import Error


T = TypeVar("T", bound="ErrorEvent")


@_attrs_define
class ErrorEvent:
    """Occurs when an [error](/docs/guides/error-codes/api-errors) occurs. This can happen due to an internal server error
    or a timeout.

        Attributes:
            event (ErrorEventEvent):
            data (Error):
    """

    event: ErrorEventEvent
    data: "Error"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        event = self.event.value

        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event": event,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error import Error

        d = src_dict.copy()
        event = ErrorEventEvent(d.pop("event"))

        data = Error.from_dict(d.pop("data"))

        error_event = cls(
            event=event,
            data=data,
        )

        error_event.additional_properties = d
        return error_event

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
