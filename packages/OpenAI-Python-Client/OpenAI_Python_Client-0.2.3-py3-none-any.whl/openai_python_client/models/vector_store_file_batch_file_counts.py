from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VectorStoreFileBatchFileCounts")


@_attrs_define
class VectorStoreFileBatchFileCounts:
    """
    Attributes:
        in_progress (int): The number of files that are currently being processed.
        completed (int): The number of files that have been processed.
        failed (int): The number of files that have failed to process.
        cancelled (int): The number of files that where cancelled.
        total (int): The total number of files.
    """

    in_progress: int
    completed: int
    failed: int
    cancelled: int
    total: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        in_progress = self.in_progress

        completed = self.completed

        failed = self.failed

        cancelled = self.cancelled

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "in_progress": in_progress,
                "completed": completed,
                "failed": failed,
                "cancelled": cancelled,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        in_progress = d.pop("in_progress")

        completed = d.pop("completed")

        failed = d.pop("failed")

        cancelled = d.pop("cancelled")

        total = d.pop("total")

        vector_store_file_batch_file_counts = cls(
            in_progress=in_progress,
            completed=completed,
            failed=failed,
            cancelled=cancelled,
            total=total,
        )

        vector_store_file_batch_file_counts.additional_properties = d
        return vector_store_file_batch_file_counts

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
