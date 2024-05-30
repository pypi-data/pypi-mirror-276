from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chat_completion_token_logprob import ChatCompletionTokenLogprob


T = TypeVar("T", bound="CreateChatCompletionResponseChoicesItemLogprobsType0")


@_attrs_define
class CreateChatCompletionResponseChoicesItemLogprobsType0:
    """Log probability information for the choice.

    Attributes:
        content (Union[List['ChatCompletionTokenLogprob'], None]): A list of message content tokens with log probability
            information.
    """

    content: Union[List["ChatCompletionTokenLogprob"], None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content: Union[List[Dict[str, Any]], None]
        if isinstance(self.content, list):
            content = []
            for content_type_0_item_data in self.content:
                content_type_0_item = content_type_0_item_data.to_dict()
                content.append(content_type_0_item)

        else:
            content = self.content

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_completion_token_logprob import ChatCompletionTokenLogprob

        d = src_dict.copy()

        def _parse_content(data: object) -> Union[List["ChatCompletionTokenLogprob"], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_0 = []
                _content_type_0 = data
                for content_type_0_item_data in _content_type_0:
                    content_type_0_item = ChatCompletionTokenLogprob.from_dict(content_type_0_item_data)

                    content_type_0.append(content_type_0_item)

                return content_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ChatCompletionTokenLogprob"], None], data)

        content = _parse_content(d.pop("content"))

        create_chat_completion_response_choices_item_logprobs_type_0 = cls(
            content=content,
        )

        create_chat_completion_response_choices_item_logprobs_type_0.additional_properties = d
        return create_chat_completion_response_choices_item_logprobs_type_0

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
