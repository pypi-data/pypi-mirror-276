from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_batches_response_object import ListBatchesResponseObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch import Batch


T = TypeVar("T", bound="ListBatchesResponse")


@_attrs_define
class ListBatchesResponse:
    """
    Attributes:
        data (List['Batch']):
        has_more (bool):
        object_ (ListBatchesResponseObject):
        first_id (Union[Unset, str]):  Example: batch_abc123.
        last_id (Union[Unset, str]):  Example: batch_abc456.
    """

    data: List["Batch"]
    has_more: bool
    object_: ListBatchesResponseObject
    first_id: Union[Unset, str] = UNSET
    last_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        has_more = self.has_more

        object_ = self.object_.value

        first_id = self.first_id

        last_id = self.last_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "has_more": has_more,
                "object": object_,
            }
        )
        if first_id is not UNSET:
            field_dict["first_id"] = first_id
        if last_id is not UNSET:
            field_dict["last_id"] = last_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch import Batch

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Batch.from_dict(data_item_data)

            data.append(data_item)

        has_more = d.pop("has_more")

        object_ = ListBatchesResponseObject(d.pop("object"))

        first_id = d.pop("first_id", UNSET)

        last_id = d.pop("last_id", UNSET)

        list_batches_response = cls(
            data=data,
            has_more=has_more,
            object_=object_,
            first_id=first_id,
            last_id=last_id,
        )

        list_batches_response.additional_properties = d
        return list_batches_response

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
