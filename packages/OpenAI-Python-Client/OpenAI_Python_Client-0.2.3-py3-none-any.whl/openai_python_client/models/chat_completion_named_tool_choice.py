from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chat_completion_named_tool_choice_type import ChatCompletionNamedToolChoiceType

if TYPE_CHECKING:
    from ..models.chat_completion_named_tool_choice_function import ChatCompletionNamedToolChoiceFunction


T = TypeVar("T", bound="ChatCompletionNamedToolChoice")


@_attrs_define
class ChatCompletionNamedToolChoice:
    """Specifies a tool the model should use. Use to force the model to call a specific function.

    Attributes:
        type (ChatCompletionNamedToolChoiceType): The type of the tool. Currently, only `function` is supported.
        function (ChatCompletionNamedToolChoiceFunction):
    """

    type: ChatCompletionNamedToolChoiceType
    function: "ChatCompletionNamedToolChoiceFunction"
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
        from ..models.chat_completion_named_tool_choice_function import ChatCompletionNamedToolChoiceFunction

        d = src_dict.copy()
        type = ChatCompletionNamedToolChoiceType(d.pop("type"))

        function = ChatCompletionNamedToolChoiceFunction.from_dict(d.pop("function"))

        chat_completion_named_tool_choice = cls(
            type=type,
            function=function,
        )

        chat_completion_named_tool_choice.additional_properties = d
        return chat_completion_named_tool_choice

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
