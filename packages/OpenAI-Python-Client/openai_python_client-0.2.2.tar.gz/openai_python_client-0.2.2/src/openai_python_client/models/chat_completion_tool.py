from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chat_completion_tool_type import ChatCompletionToolType

if TYPE_CHECKING:
    from ..models.function_object import FunctionObject


T = TypeVar("T", bound="ChatCompletionTool")


@_attrs_define
class ChatCompletionTool:
    """
    Attributes:
        type (ChatCompletionToolType): The type of the tool. Currently, only `function` is supported.
        function (FunctionObject):
    """

    type: ChatCompletionToolType
    function: "FunctionObject"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        function = self.function.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "function": function,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.function_object import FunctionObject

        d = src_dict.copy()
        type = ChatCompletionToolType(d.pop("type"))

        function = FunctionObject.from_dict(d.pop("function"))

        chat_completion_tool = cls(
            type=type,
            function=function,
        )

        chat_completion_tool.additional_properties = d
        return chat_completion_tool

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
