from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_tool_call_object_type import RunToolCallObjectType

if TYPE_CHECKING:
    from ..models.run_tool_call_object_function import RunToolCallObjectFunction


T = TypeVar("T", bound="RunToolCallObject")


@_attrs_define
class RunToolCallObject:
    """Tool call objects

    Attributes:
        id (str): The ID of the tool call. This ID must be referenced when you submit the tool outputs in using the
            [Submit tool outputs to run](/docs/api-reference/runs/submitToolOutputs) endpoint.
        type (RunToolCallObjectType): The type of tool call the output is required for. For now, this is always
            `function`.
        function (RunToolCallObjectFunction): The function definition.
    """

    id: str
    type: RunToolCallObjectType
    function: "RunToolCallObjectFunction"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        type = self.type.value

        function = self.function.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "function": function,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_tool_call_object_function import RunToolCallObjectFunction

        d = src_dict.copy()
        id = d.pop("id")

        type = RunToolCallObjectType(d.pop("type"))

        function = RunToolCallObjectFunction.from_dict(d.pop("function"))

        run_tool_call_object = cls(
            id=id,
            type=type,
            function=function,
        )

        run_tool_call_object.additional_properties = d
        return run_tool_call_object

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
