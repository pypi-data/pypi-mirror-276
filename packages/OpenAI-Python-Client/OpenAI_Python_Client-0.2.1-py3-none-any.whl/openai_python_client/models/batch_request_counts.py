from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BatchRequestCounts")


@_attrs_define
class BatchRequestCounts:
    """The request counts for different statuses within the batch.

    Attributes:
        total (int): Total number of requests in the batch.
        completed (int): Number of requests that have been completed successfully.
        failed (int): Number of requests that have failed.
    """

    total: int
    completed: int
    failed: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total = self.total

        completed = self.completed

        failed = self.failed

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "completed": completed,
                "failed": failed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total = d.pop("total")

        completed = d.pop("completed")

        failed = d.pop("failed")

        batch_request_counts = cls(
            total=total,
            completed=completed,
            failed=failed,
        )

        batch_request_counts.additional_properties = d
        return batch_request_counts

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
