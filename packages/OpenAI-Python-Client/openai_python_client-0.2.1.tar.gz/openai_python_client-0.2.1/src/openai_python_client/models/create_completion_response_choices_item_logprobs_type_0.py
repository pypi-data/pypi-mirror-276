from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_completion_response_choices_item_logprobs_type_0_top_logprobs_item import (
        CreateCompletionResponseChoicesItemLogprobsType0TopLogprobsItem,
    )


T = TypeVar("T", bound="CreateCompletionResponseChoicesItemLogprobsType0")


@_attrs_define
class CreateCompletionResponseChoicesItemLogprobsType0:
    """
    Attributes:
        text_offset (Union[Unset, List[int]]):
        token_logprobs (Union[Unset, List[float]]):
        tokens (Union[Unset, List[str]]):
        top_logprobs (Union[Unset, List['CreateCompletionResponseChoicesItemLogprobsType0TopLogprobsItem']]):
    """

    text_offset: Union[Unset, List[int]] = UNSET
    token_logprobs: Union[Unset, List[float]] = UNSET
    tokens: Union[Unset, List[str]] = UNSET
    top_logprobs: Union[Unset, List["CreateCompletionResponseChoicesItemLogprobsType0TopLogprobsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        text_offset: Union[Unset, List[int]] = UNSET
        if not isinstance(self.text_offset, Unset):
            text_offset = self.text_offset

        token_logprobs: Union[Unset, List[float]] = UNSET
        if not isinstance(self.token_logprobs, Unset):
            token_logprobs = self.token_logprobs

        tokens: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tokens, Unset):
            tokens = self.tokens

        top_logprobs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.top_logprobs, Unset):
            top_logprobs = []
            for top_logprobs_item_data in self.top_logprobs:
                top_logprobs_item = top_logprobs_item_data.to_dict()
                top_logprobs.append(top_logprobs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if text_offset is not UNSET:
            field_dict["text_offset"] = text_offset
        if token_logprobs is not UNSET:
            field_dict["token_logprobs"] = token_logprobs
        if tokens is not UNSET:
            field_dict["tokens"] = tokens
        if top_logprobs is not UNSET:
            field_dict["top_logprobs"] = top_logprobs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_completion_response_choices_item_logprobs_type_0_top_logprobs_item import (
            CreateCompletionResponseChoicesItemLogprobsType0TopLogprobsItem,
        )

        d = src_dict.copy()
        text_offset = cast(List[int], d.pop("text_offset", UNSET))

        token_logprobs = cast(List[float], d.pop("token_logprobs", UNSET))

        tokens = cast(List[str], d.pop("tokens", UNSET))

        top_logprobs = []
        _top_logprobs = d.pop("top_logprobs", UNSET)
        for top_logprobs_item_data in _top_logprobs or []:
            top_logprobs_item = CreateCompletionResponseChoicesItemLogprobsType0TopLogprobsItem.from_dict(
                top_logprobs_item_data
            )

            top_logprobs.append(top_logprobs_item)

        create_completion_response_choices_item_logprobs_type_0 = cls(
            text_offset=text_offset,
            token_logprobs=token_logprobs,
            tokens=tokens,
            top_logprobs=top_logprobs,
        )

        create_completion_response_choices_item_logprobs_type_0.additional_properties = d
        return create_completion_response_choices_item_logprobs_type_0

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
