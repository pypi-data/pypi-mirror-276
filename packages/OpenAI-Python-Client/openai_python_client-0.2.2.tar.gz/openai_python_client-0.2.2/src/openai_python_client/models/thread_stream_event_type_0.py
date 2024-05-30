from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.thread_stream_event_type_0_event import ThreadStreamEventType0Event

if TYPE_CHECKING:
    from ..models.thread import Thread


T = TypeVar("T", bound="ThreadStreamEventType0")


@_attrs_define
class ThreadStreamEventType0:
    """Occurs when a new [thread](/docs/api-reference/threads/object) is created.

    Attributes:
        event (ThreadStreamEventType0Event):
        data (Thread): Represents a thread that contains [messages](/docs/api-reference/messages).
    """

    event: ThreadStreamEventType0Event
    data: "Thread"
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
        from ..models.thread import Thread

        d = src_dict.copy()
        event = ThreadStreamEventType0Event(d.pop("event"))

        data = Thread.from_dict(d.pop("data"))

        thread_stream_event_type_0 = cls(
            event=event,
            data=data,
        )

        thread_stream_event_type_0.additional_properties = d
        return thread_stream_event_type_0

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
