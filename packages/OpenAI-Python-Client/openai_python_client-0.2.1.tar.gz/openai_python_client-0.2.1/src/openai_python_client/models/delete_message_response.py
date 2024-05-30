from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delete_message_response_object import DeleteMessageResponseObject

T = TypeVar("T", bound="DeleteMessageResponse")


@_attrs_define
class DeleteMessageResponse:
    """
    Attributes:
        id (str):
        deleted (bool):
        object_ (DeleteMessageResponseObject):
    """

    id: str
    deleted: bool
    object_: DeleteMessageResponseObject
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        deleted = self.deleted

        object_ = self.object_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "deleted": deleted,
                "object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        deleted = d.pop("deleted")

        object_ = DeleteMessageResponseObject(d.pop("object"))

        delete_message_response = cls(
            id=id,
            deleted=deleted,
            object_=object_,
        )

        delete_message_response.additional_properties = d
        return delete_message_response

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
