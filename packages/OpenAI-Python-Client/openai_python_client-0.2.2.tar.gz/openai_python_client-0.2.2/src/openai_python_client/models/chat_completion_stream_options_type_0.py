from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatCompletionStreamOptionsType0")


@_attrs_define
class ChatCompletionStreamOptionsType0:
    """Options for streaming response. Only set this when you set `stream: true`.

    Attributes:
        include_usage (Union[Unset, bool]): If set, an additional chunk will be streamed before the `data: [DONE]`
            message. The `usage` field on this chunk shows the token usage statistics for the entire request, and the
            `choices` field will always be an empty array. All other chunks will also include a `usage` field, but with a
            null value.
    """

    include_usage: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        include_usage = self.include_usage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include_usage is not UNSET:
            field_dict["include_usage"] = include_usage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        include_usage = d.pop("include_usage", UNSET)

        chat_completion_stream_options_type_0 = cls(
            include_usage=include_usage,
        )

        chat_completion_stream_options_type_0.additional_properties = d
        return chat_completion_stream_options_type_0

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
