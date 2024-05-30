from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.message_creation_type import MessageCreationType

if TYPE_CHECKING:
    from ..models.message_creation_message_creation import MessageCreationMessageCreation


T = TypeVar("T", bound="MessageCreation")


@_attrs_define
class MessageCreation:
    """Details of the message creation by the run step.

    Attributes:
        type (MessageCreationType): Always `message_creation`.
        message_creation (MessageCreationMessageCreation):
    """

    type: MessageCreationType
    message_creation: "MessageCreationMessageCreation"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        message_creation = self.message_creation.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "message_creation": message_creation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_creation_message_creation import MessageCreationMessageCreation

        d = src_dict.copy()
        type = MessageCreationType(d.pop("type"))

        message_creation = MessageCreationMessageCreation.from_dict(d.pop("message_creation"))

        message_creation = cls(
            type=type,
            message_creation=message_creation,
        )

        message_creation.additional_properties = d
        return message_creation

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
