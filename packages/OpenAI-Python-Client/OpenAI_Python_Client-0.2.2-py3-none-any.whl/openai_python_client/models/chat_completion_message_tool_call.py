from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chat_completion_message_tool_call_type import ChatCompletionMessageToolCallType

if TYPE_CHECKING:
    from ..models.chat_completion_message_tool_call_function import ChatCompletionMessageToolCallFunction


T = TypeVar("T", bound="ChatCompletionMessageToolCall")


@_attrs_define
class ChatCompletionMessageToolCall:
    """
    Attributes:
        id (str): The ID of the tool call.
        type (ChatCompletionMessageToolCallType): The type of the tool. Currently, only `function` is supported.
        function (ChatCompletionMessageToolCallFunction): The function that the model called.
    """

    id: str
    type: ChatCompletionMessageToolCallType
    function: "ChatCompletionMessageToolCallFunction"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        type = self.type.value

        function = self.function.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "function": function,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_completion_message_tool_call_function import ChatCompletionMessageToolCallFunction

        d = src_dict.copy()
        id = d.pop("id")

        type = ChatCompletionMessageToolCallType(d.pop("type"))

        function = ChatCompletionMessageToolCallFunction.from_dict(d.pop("function"))

        chat_completion_message_tool_call = cls(
            id=id,
            type=type,
            function=function,
        )

        chat_completion_message_tool_call.additional_properties = d
        return chat_completion_message_tool_call

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
