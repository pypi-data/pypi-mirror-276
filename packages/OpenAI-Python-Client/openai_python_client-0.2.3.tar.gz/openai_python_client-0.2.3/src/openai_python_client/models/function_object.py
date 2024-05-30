from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_parameters import FunctionParameters


T = TypeVar("T", bound="FunctionObject")


@_attrs_define
class FunctionObject:
    """
    Attributes:
        name (str): The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes,
            with a maximum length of 64.
        description (Union[Unset, str]): A description of what the function does, used by the model to choose when and
            how to call the function.
        parameters (Union[Unset, FunctionParameters]): The parameters the functions accepts, described as a JSON Schema
            object. See the [guide](/docs/guides/text-generation/function-calling) for examples, and the [JSON Schema
            reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

            Omitting `parameters` defines a function with an empty parameter list.
    """

    name: str
    description: Union[Unset, str] = UNSET
    parameters: Union[Unset, "FunctionParameters"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.function_parameters import FunctionParameters

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, FunctionParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = FunctionParameters.from_dict(_parameters)

        function_object = cls(
            name=name,
            description=description,
            parameters=parameters,
        )

        function_object.additional_properties = d
        return function_object

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
