from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmitToolOutputsRunRequestToolOutputsItem")


@_attrs_define
class SubmitToolOutputsRunRequestToolOutputsItem:
    """
    Attributes:
        tool_call_id (Union[Unset, str]): The ID of the tool call in the `required_action` object within the run object
            the output is being submitted for.
        output (Union[Unset, str]): The output of the tool call to be submitted to continue the run.
    """

    tool_call_id: Union[Unset, str] = UNSET
    output: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tool_call_id = self.tool_call_id

        output = self.output

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tool_call_id is not UNSET:
            field_dict["tool_call_id"] = tool_call_id
        if output is not UNSET:
            field_dict["output"] = output

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tool_call_id = d.pop("tool_call_id", UNSET)

        output = d.pop("output", UNSET)

        submit_tool_outputs_run_request_tool_outputs_item = cls(
            tool_call_id=tool_call_id,
            output=output,
        )

        submit_tool_outputs_run_request_tool_outputs_item.additional_properties = d
        return submit_tool_outputs_run_request_tool_outputs_item

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
