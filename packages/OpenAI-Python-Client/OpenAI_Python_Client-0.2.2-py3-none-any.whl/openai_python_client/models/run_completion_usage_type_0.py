from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RunCompletionUsageType0")


@_attrs_define
class RunCompletionUsageType0:
    """Usage statistics related to the run. This value will be `null` if the run is not in a terminal state (i.e.
    `in_progress`, `queued`, etc.).

        Attributes:
            completion_tokens (int): Number of completion tokens used over the course of the run.
            prompt_tokens (int): Number of prompt tokens used over the course of the run.
            total_tokens (int): Total number of tokens used (prompt + completion).
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

        run_completion_usage_type_0 = cls(
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens,
            total_tokens=total_tokens,
        )

        run_completion_usage_type_0.additional_properties = d
        return run_completion_usage_type_0

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
