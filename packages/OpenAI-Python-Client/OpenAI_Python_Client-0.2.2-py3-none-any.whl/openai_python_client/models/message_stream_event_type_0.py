from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.message_stream_event_type_0_event import MessageStreamEventType0Event

if TYPE_CHECKING:
    from ..models.the_message_object import TheMessageObject


T = TypeVar("T", bound="MessageStreamEventType0")


@_attrs_define
class MessageStreamEventType0:
    """Occurs when a [message](/docs/api-reference/messages/object) is created.

    Attributes:
        event (MessageStreamEventType0Event):
        data (TheMessageObject): Represents a message within a [thread](/docs/api-reference/threads).
    """

    event: MessageStreamEventType0Event
    data: "TheMessageObject"
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
        from ..models.the_message_object import TheMessageObject

        d = src_dict.copy()
        event = MessageStreamEventType0Event(d.pop("event"))

        data = TheMessageObject.from_dict(d.pop("data"))

        message_stream_event_type_0 = cls(
            event=event,
            data=data,
        )

        message_stream_event_type_0.additional_properties = d
        return message_stream_event_type_0

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
