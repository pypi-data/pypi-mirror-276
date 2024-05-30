from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_paginated_fine_tuning_jobs_response_object import ListPaginatedFineTuningJobsResponseObject

if TYPE_CHECKING:
    from ..models.fine_tuning_job import FineTuningJob


T = TypeVar("T", bound="ListPaginatedFineTuningJobsResponse")


@_attrs_define
class ListPaginatedFineTuningJobsResponse:
    """
    Attributes:
        data (List['FineTuningJob']):
        has_more (bool):
        object_ (ListPaginatedFineTuningJobsResponseObject):
    """

    data: List["FineTuningJob"]
    has_more: bool
    object_: ListPaginatedFineTuningJobsResponseObject
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        has_more = self.has_more

        object_ = self.object_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "has_more": has_more,
                "object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fine_tuning_job import FineTuningJob

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = FineTuningJob.from_dict(data_item_data)

            data.append(data_item)

        has_more = d.pop("has_more")

        object_ = ListPaginatedFineTuningJobsResponseObject(d.pop("object"))

        list_paginated_fine_tuning_jobs_response = cls(
            data=data,
            has_more=has_more,
            object_=object_,
        )

        list_paginated_fine_tuning_jobs_response.additional_properties = d
        return list_paginated_fine_tuning_jobs_response

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
