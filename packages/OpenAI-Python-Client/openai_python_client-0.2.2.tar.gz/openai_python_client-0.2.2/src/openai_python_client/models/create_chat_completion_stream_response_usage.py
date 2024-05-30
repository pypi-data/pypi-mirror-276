from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateChatCompletionStreamResponseUsage")


@_attrs_define
class CreateChatCompletionStreamResponseUsage:
    """An optional field that will only be present when you set `stream_options: {"include_usage": true}` in your request.
    When present, it contains a null value except for the last chunk which contains the token usage statistics for the
    entire request.

        Attributes:
            completion_tokens (int): Number of tokens in the generated completion.
            prompt_tokens (int): Number of tokens in the prompt.
            total_tokens (int): Total number of tokens used in the request (prompt + completion).
    """

    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        completion_tokens = self.completion_tokens

        prompt_tokens = self.prompt_tokens

        total_tokens = self.total_tokens

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completion_tokens": completion_tokens,
                "prompt_tokens": prompt_tokens,
                "total_tokens": total_tokens,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        completion_tokens = d.pop("completion_tokens")

        prompt_tokens = d.pop("prompt_tokens")

        total_tokens = d.pop("total_tokens")

        create_chat_completion_stream_response_usage = cls(
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens,
            total_tokens=total_tokens,
        )

        create_chat_completion_stream_response_usage.additional_properties = d
        return create_chat_completion_stream_response_usage

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
