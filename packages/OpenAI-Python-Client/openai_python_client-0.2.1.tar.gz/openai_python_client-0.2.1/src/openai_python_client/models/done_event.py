from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.done_event_data import DoneEventData
from ..models.done_event_event import DoneEventEvent

T = TypeVar("T", bound="DoneEvent")


@_attrs_define
class DoneEvent:
    """Occurs when a stream ends.

    Attributes:
        event (DoneEventEvent):
        data (DoneEventData):
    """

    event: DoneEventEvent
    data: DoneEventData
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        event = self.event.value

        data = self.data.value

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
        d = src_dict.copy()
        event = DoneEventEvent(d.pop("event"))

        data = DoneEventData(d.pop("data"))

        done_event = cls(
            event=event,
            data=data,
        )

        done_event.additional_properties = d
        return done_event

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
