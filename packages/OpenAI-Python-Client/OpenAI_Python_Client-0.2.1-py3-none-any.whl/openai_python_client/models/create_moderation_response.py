from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_moderation_response_results_item import CreateModerationResponseResultsItem


T = TypeVar("T", bound="CreateModerationResponse")


@_attrs_define
class CreateModerationResponse:
    """Represents if a given text input is potentially harmful.

    Attributes:
        id (str): The unique identifier for the moderation request.
        model (str): The model used to generate the moderation results.
        results (List['CreateModerationResponseResultsItem']): A list of moderation objects.
    """

    id: str
    model: str
    results: List["CreateModerationResponseResultsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        model = self.model

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "model": model,
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_moderation_response_results_item import CreateModerationResponseResultsItem

        d = src_dict.copy()
        id = d.pop("id")

        model = d.pop("model")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = CreateModerationResponseResultsItem.from_dict(results_item_data)

            results.append(results_item)

        create_moderation_response = cls(
            id=id,
            model=model,
            results=results,
        )

        create_moderation_response.additional_properties = d
        return create_moderation_response

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
