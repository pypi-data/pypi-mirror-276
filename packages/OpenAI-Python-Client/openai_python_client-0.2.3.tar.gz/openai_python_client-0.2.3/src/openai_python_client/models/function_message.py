from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.function_message_role import FunctionMessageRole

T = TypeVar("T", bound="FunctionMessage")


@_attrs_define
class FunctionMessage:
    """
    Attributes:
        role (FunctionMessageRole): The role of the messages author, in this case `function`.
        content (Union[None, str]): The contents of the function message.
        name (str): The name of the function to call.
    """

    role: FunctionMessageRole
    content: Union[None, str]
    name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role.value

        content: Union[None, str]
        content = self.content

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "content": content,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = FunctionMessageRole(d.pop("role"))

        def _parse_content(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        content = _parse_content(d.pop("content"))

        name = d.pop("name")

        function_message = cls(
            role=role,
            content=content,
            name=name,
        )

        function_message.additional_properties = d
        return function_message

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
