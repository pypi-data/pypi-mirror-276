from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.the_message_object import TheMessageObject


T = TypeVar("T", bound="ListMessagesResponse")


@_attrs_define
class ListMessagesResponse:
    """
    Attributes:
        object_ (str):  Example: list.
        data (List['TheMessageObject']):
        first_id (str):  Example: msg_abc123.
        last_id (str):  Example: msg_abc123.
        has_more (bool):
    """

    object_: str
    data: List["TheMessageObject"]
    first_id: str
    last_id: str
    has_more: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        first_id = self.first_id

        last_id = self.last_id

        has_more = self.has_more

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "data": data,
                "first_id": first_id,
                "last_id": last_id,
                "has_more": has_more,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.the_message_object import TheMessageObject

        d = src_dict.copy()
        object_ = d.pop("object")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = TheMessageObject.from_dict(data_item_data)

            data.append(data_item)

        first_id = d.pop("first_id")

        last_id = d.pop("last_id")

        has_more = d.pop("has_more")

        list_messages_response = cls(
            object_=object_,
            data=data,
            first_id=first_id,
            last_id=last_id,
            has_more=has_more,
        )

        list_messages_response.additional_properties = d
        return list_messages_response

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
