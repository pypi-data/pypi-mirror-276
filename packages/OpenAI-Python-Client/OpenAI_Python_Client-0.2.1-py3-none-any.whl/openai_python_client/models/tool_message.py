from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tool_message_role import ToolMessageRole

T = TypeVar("T", bound="ToolMessage")


@_attrs_define
class ToolMessage:
    """
    Attributes:
        role (ToolMessageRole): The role of the messages author, in this case `tool`.
        content (str): The contents of the tool message.
        tool_call_id (str): Tool call that this message is responding to.
    """

    role: ToolMessageRole
    content: str
    tool_call_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role.value

        content = self.content

        tool_call_id = self.tool_call_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "content": content,
                "tool_call_id": tool_call_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = ToolMessageRole(d.pop("role"))

        content = d.pop("content")

        tool_call_id = d.pop("tool_call_id")

        tool_message = cls(
            role=role,
            content=content,
            tool_call_id=tool_call_id,
        )

        tool_message.additional_properties = d
        return tool_message

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
