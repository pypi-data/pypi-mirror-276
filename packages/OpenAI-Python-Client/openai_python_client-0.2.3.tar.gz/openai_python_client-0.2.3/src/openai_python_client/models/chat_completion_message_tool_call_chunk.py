from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chat_completion_message_tool_call_chunk_type import ChatCompletionMessageToolCallChunkType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_completion_message_tool_call_chunk_function import ChatCompletionMessageToolCallChunkFunction


T = TypeVar("T", bound="ChatCompletionMessageToolCallChunk")


@_attrs_define
class ChatCompletionMessageToolCallChunk:
    """
    Attributes:
        index (int):
        id (Union[Unset, str]): The ID of the tool call.
        type (Union[Unset, ChatCompletionMessageToolCallChunkType]): The type of the tool. Currently, only `function` is
            supported.
        function (Union[Unset, ChatCompletionMessageToolCallChunkFunction]):
    """

    index: int
    id: Union[Unset, str] = UNSET
    type: Union[Unset, ChatCompletionMessageToolCallChunkType] = UNSET
    function: Union[Unset, "ChatCompletionMessageToolCallChunkFunction"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        index = self.index

        id = self.id

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        function: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.function, Unset):
            function = self.function.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index": index,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if type is not UNSET:
            field_dict["type"] = type
        if function is not UNSET:
            field_dict["function"] = function

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_completion_message_tool_call_chunk_function import ChatCompletionMessageToolCallChunkFunction

        d = src_dict.copy()
        index = d.pop("index")

        id = d.pop("id", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ChatCompletionMessageToolCallChunkType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ChatCompletionMessageToolCallChunkType(_type)

        _function = d.pop("function", UNSET)
        function: Union[Unset, ChatCompletionMessageToolCallChunkFunction]
        if isinstance(_function, Unset):
            function = UNSET
        else:
            function = ChatCompletionMessageToolCallChunkFunction.from_dict(_function)

        chat_completion_message_tool_call_chunk = cls(
            index=index,
            id=id,
            type=type,
            function=function,
        )

        chat_completion_message_tool_call_chunk.additional_properties = d
        return chat_completion_message_tool_call_chunk

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
