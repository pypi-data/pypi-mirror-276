from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.system_message_role import SystemMessageRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="SystemMessage")


@_attrs_define
class SystemMessage:
    """
    Attributes:
        content (str): The contents of the system message.
        role (SystemMessageRole): The role of the messages author, in this case `system`.
        name (Union[Unset, str]): An optional name for the participant. Provides the model information to differentiate
            between participants of the same role.
    """

    content: str
    role: SystemMessageRole
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content

        role = self.role.value

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "role": role,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content")

        role = SystemMessageRole(d.pop("role"))

        name = d.pop("name", UNSET)

        system_message = cls(
            content=content,
            role=role,
            name=name,
        )

        system_message.additional_properties = d
        return system_message

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
