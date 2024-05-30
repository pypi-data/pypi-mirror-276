from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_chat_completion_stream_response_object import CreateChatCompletionStreamResponseObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_chat_completion_stream_response_choices_item import (
        CreateChatCompletionStreamResponseChoicesItem,
    )
    from ..models.create_chat_completion_stream_response_usage import CreateChatCompletionStreamResponseUsage


T = TypeVar("T", bound="CreateChatCompletionStreamResponse")


@_attrs_define
class CreateChatCompletionStreamResponse:
    """Represents a streamed chunk of a chat completion response returned by model, based on the provided input.

    Attributes:
        id (str): A unique identifier for the chat completion. Each chunk has the same ID.
        choices (List['CreateChatCompletionStreamResponseChoicesItem']): A list of chat completion choices. Can contain
            more than one elements if `n` is greater than 1. Can also be empty for the
            last chunk if you set `stream_options: {"include_usage": true}`.
        created (int): The Unix timestamp (in seconds) of when the chat completion was created. Each chunk has the same
            timestamp.
        model (str): The model to generate the completion.
        object_ (CreateChatCompletionStreamResponseObject): The object type, which is always `chat.completion.chunk`.
        system_fingerprint (Union[Unset, str]): This fingerprint represents the backend configuration that the model
            runs with.
            Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made
            that might impact determinism.
        usage (Union[Unset, CreateChatCompletionStreamResponseUsage]): An optional field that will only be present when
            you set `stream_options: {"include_usage": true}` in your request.
            When present, it contains a null value except for the last chunk which contains the token usage statistics for
            the entire request.
    """

    id: str
    choices: List["CreateChatCompletionStreamResponseChoicesItem"]
    created: int
    model: str
    object_: CreateChatCompletionStreamResponseObject
    system_fingerprint: Union[Unset, str] = UNSET
    usage: Union[Unset, "CreateChatCompletionStreamResponseUsage"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        choices = []
        for choices_item_data in self.choices:
            choices_item = choices_item_data.to_dict()
            choices.append(choices_item)

        created = self.created

        model = self.model

        object_ = self.object_.value

        system_fingerprint = self.system_fingerprint

        usage: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "choices": choices,
                "created": created,
                "model": model,
                "object": object_,
            }
        )
        if system_fingerprint is not UNSET:
            field_dict["system_fingerprint"] = system_fingerprint
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_chat_completion_stream_response_choices_item import (
            CreateChatCompletionStreamResponseChoicesItem,
        )
        from ..models.create_chat_completion_stream_response_usage import CreateChatCompletionStreamResponseUsage

        d = src_dict.copy()
        id = d.pop("id")

        choices = []
        _choices = d.pop("choices")
        for choices_item_data in _choices:
            choices_item = CreateChatCompletionStreamResponseChoicesItem.from_dict(choices_item_data)

            choices.append(choices_item)

        created = d.pop("created")

        model = d.pop("model")

        object_ = CreateChatCompletionStreamResponseObject(d.pop("object"))

        system_fingerprint = d.pop("system_fingerprint", UNSET)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, CreateChatCompletionStreamResponseUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = CreateChatCompletionStreamResponseUsage.from_dict(_usage)

        create_chat_completion_stream_response = cls(
            id=id,
            choices=choices,
            created=created,
            model=model,
            object_=object_,
            system_fingerprint=system_fingerprint,
            usage=usage,
        )

        create_chat_completion_stream_response.additional_properties = d
        return create_chat_completion_stream_response

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
