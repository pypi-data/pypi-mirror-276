from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FunctionToolCallFunction")


@_attrs_define
class FunctionToolCallFunction:
    """The definition of the function that was called.

    Attributes:
        name (str): The name of the function.
        arguments (str): The arguments passed to the function.
        output (Union[None, str]): The output of the function. This will be `null` if the outputs have not been
            [submitted](/docs/api-reference/runs/submitToolOutputs) yet.
    """

    name: str
    arguments: str
    output: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        arguments = self.arguments

        output: Union[None, str]
        output = self.output

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "arguments": arguments,
                "output": output,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        arguments = d.pop("arguments")

        def _parse_output(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        output = _parse_output(d.pop("output"))

        function_tool_call_function = cls(
            name=name,
            arguments=arguments,
            output=output,
        )

        function_tool_call_function.additional_properties = d
        return function_tool_call_function

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
