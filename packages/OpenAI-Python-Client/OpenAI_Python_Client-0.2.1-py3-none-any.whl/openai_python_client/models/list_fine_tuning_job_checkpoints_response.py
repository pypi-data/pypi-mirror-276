from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_fine_tuning_job_checkpoints_response_object import ListFineTuningJobCheckpointsResponseObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fine_tuning_job_checkpoint import FineTuningJobCheckpoint


T = TypeVar("T", bound="ListFineTuningJobCheckpointsResponse")


@_attrs_define
class ListFineTuningJobCheckpointsResponse:
    """
    Attributes:
        data (List['FineTuningJobCheckpoint']):
        object_ (ListFineTuningJobCheckpointsResponseObject):
        has_more (bool):
        first_id (Union[None, Unset, str]):
        last_id (Union[None, Unset, str]):
    """

    data: List["FineTuningJobCheckpoint"]
    object_: ListFineTuningJobCheckpointsResponseObject
    has_more: bool
    first_id: Union[None, Unset, str] = UNSET
    last_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        object_ = self.object_.value

        has_more = self.has_more

        first_id: Union[None, Unset, str]
        if isinstance(self.first_id, Unset):
            first_id = UNSET
        else:
            first_id = self.first_id

        last_id: Union[None, Unset, str]
        if isinstance(self.last_id, Unset):
            last_id = UNSET
        else:
            last_id = self.last_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "object": object_,
                "has_more": has_more,
            }
        )
        if first_id is not UNSET:
            field_dict["first_id"] = first_id
        if last_id is not UNSET:
            field_dict["last_id"] = last_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fine_tuning_job_checkpoint import FineTuningJobCheckpoint

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = FineTuningJobCheckpoint.from_dict(data_item_data)

            data.append(data_item)

        object_ = ListFineTuningJobCheckpointsResponseObject(d.pop("object"))

        has_more = d.pop("has_more")

        def _parse_first_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        first_id = _parse_first_id(d.pop("first_id", UNSET))

        def _parse_last_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        last_id = _parse_last_id(d.pop("last_id", UNSET))

        list_fine_tuning_job_checkpoints_response = cls(
            data=data,
            object_=object_,
            has_more=has_more,
            first_id=first_id,
            last_id=last_id,
        )

        list_fine_tuning_job_checkpoints_response.additional_properties = d
        return list_fine_tuning_job_checkpoints_response

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
