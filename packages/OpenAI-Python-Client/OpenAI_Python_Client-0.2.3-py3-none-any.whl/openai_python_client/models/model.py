from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_object import ModelObject

T = TypeVar("T", bound="Model")


@_attrs_define
class Model:
    """Describes an OpenAI model offering that can be used with the API.

    Attributes:
        id (str): The model identifier, which can be referenced in the API endpoints.
        created (int): The Unix timestamp (in seconds) when the model was created.
        object_ (ModelObject): The object type, which is always "model".
        owned_by (str): The organization that owns the model.
    """

    id: str
    created: int
    object_: ModelObject
    owned_by: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created = self.created

        object_ = self.object_.value

        owned_by = self.owned_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created": created,
                "object": object_,
                "owned_by": owned_by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created = d.pop("created")

        object_ = ModelObject(d.pop("object"))

        owned_by = d.pop("owned_by")

        model = cls(
            id=id,
            created=created,
            object_=object_,
            owned_by=owned_by,
        )

        model.additional_properties = d
        return model

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
