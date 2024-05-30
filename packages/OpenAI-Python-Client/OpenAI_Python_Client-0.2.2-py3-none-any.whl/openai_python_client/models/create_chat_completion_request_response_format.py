from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_chat_completion_request_response_format_type import CreateChatCompletionRequestResponseFormatType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateChatCompletionRequestResponseFormat")


@_attrs_define
class CreateChatCompletionRequestResponseFormat:
    """An object specifying the format that the model must output. Compatible with [GPT-4 Turbo](/docs/models/gpt-4-and-
    gpt-4-turbo) and all GPT-3.5 Turbo models newer than `gpt-3.5-turbo-1106`.

    Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the message the model generates is valid
    JSON.

    **Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or
    user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the
    token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be
    partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the
    conversation exceeded the max context length.

        Attributes:
            type (Union[Unset, CreateChatCompletionRequestResponseFormatType]): Must be one of `text` or `json_object`.
                Default: CreateChatCompletionRequestResponseFormatType.TEXT. Example: json_object.
    """

    type: Union[Unset, CreateChatCompletionRequestResponseFormatType] = (
        CreateChatCompletionRequestResponseFormatType.TEXT
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, CreateChatCompletionRequestResponseFormatType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = CreateChatCompletionRequestResponseFormatType(_type)

        create_chat_completion_request_response_format = cls(
            type=type,
        )

        create_chat_completion_request_response_format.additional_properties = d
        return create_chat_completion_request_response_format

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
