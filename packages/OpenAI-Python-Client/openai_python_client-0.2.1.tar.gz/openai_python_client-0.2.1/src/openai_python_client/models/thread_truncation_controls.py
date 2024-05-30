from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.thread_truncation_controls_type import ThreadTruncationControlsType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ThreadTruncationControls")


@_attrs_define
class ThreadTruncationControls:
    """Controls for how a thread will be truncated prior to the run. Use this to control the intial context window of the
    run.

        Attributes:
            type (ThreadTruncationControlsType): The truncation strategy to use for the thread. The default is `auto`. If
                set to `last_messages`, the thread will be truncated to the n most recent messages in the thread. When set to
                `auto`, messages in the middle of the thread will be dropped to fit the context length of the model,
                `max_prompt_tokens`.
            last_messages (Union[None, Unset, int]): The number of most recent messages from the thread when constructing
                the context for the run.
    """

    type: ThreadTruncationControlsType
    last_messages: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        last_messages: Union[None, Unset, int]
        if isinstance(self.last_messages, Unset):
            last_messages = UNSET
        else:
            last_messages = self.last_messages

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if last_messages is not UNSET:
            field_dict["last_messages"] = last_messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = ThreadTruncationControlsType(d.pop("type"))

        def _parse_last_messages(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        last_messages = _parse_last_messages(d.pop("last_messages", UNSET))

        thread_truncation_controls = cls(
            type=type,
            last_messages=last_messages,
        )

        thread_truncation_controls.additional_properties = d
        return thread_truncation_controls

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
