from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.run_tool_call_object import RunToolCallObject


T = TypeVar("T", bound="ARunOnAThreadRequiredActionType0SubmitToolOutputs")


@_attrs_define
class ARunOnAThreadRequiredActionType0SubmitToolOutputs:
    """Details on the tool outputs needed for this run to continue.

    Attributes:
        tool_calls (List['RunToolCallObject']): A list of the relevant tool calls.
    """

    tool_calls: List["RunToolCallObject"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tool_calls = []
        for tool_calls_item_data in self.tool_calls:
            tool_calls_item = tool_calls_item_data.to_dict()
            tool_calls.append(tool_calls_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tool_calls": tool_calls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_tool_call_object import RunToolCallObject

        d = src_dict.copy()
        tool_calls = []
        _tool_calls = d.pop("tool_calls")
        for tool_calls_item_data in _tool_calls:
            tool_calls_item = RunToolCallObject.from_dict(tool_calls_item_data)

            tool_calls.append(tool_calls_item)

        a_run_on_a_thread_required_action_type_0_submit_tool_outputs = cls(
            tool_calls=tool_calls,
        )

        a_run_on_a_thread_required_action_type_0_submit_tool_outputs.additional_properties = d
        return a_run_on_a_thread_required_action_type_0_submit_tool_outputs

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
