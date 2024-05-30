from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_models_response_object import ListModelsResponseObject

if TYPE_CHECKING:
    from ..models.model import Model


T = TypeVar("T", bound="ListModelsResponse")


@_attrs_define
class ListModelsResponse:
    """
    Attributes:
        object_ (ListModelsResponseObject):
        data (List['Model']):
    """

    object_: ListModelsResponseObject
    data: List["Model"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model import Model

        d = src_dict.copy()
        object_ = ListModelsResponseObject(d.pop("object"))

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Model.from_dict(data_item_data)

            data.append(data_item)

        list_models_response = cls(
            object_=object_,
            data=data,
        )

        list_models_response.additional_properties = d
        return list_models_response

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
