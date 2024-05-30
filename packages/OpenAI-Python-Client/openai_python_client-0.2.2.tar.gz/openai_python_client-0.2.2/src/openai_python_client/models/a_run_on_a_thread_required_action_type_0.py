from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.a_run_on_a_thread_required_action_type_0_type import ARunOnAThreadRequiredActionType0Type

if TYPE_CHECKING:
    from ..models.a_run_on_a_thread_required_action_type_0_submit_tool_outputs import (
        ARunOnAThreadRequiredActionType0SubmitToolOutputs,
    )


T = TypeVar("T", bound="ARunOnAThreadRequiredActionType0")


@_attrs_define
class ARunOnAThreadRequiredActionType0:
    """Details on the action required to continue the run. Will be `null` if no action is required.

    Attributes:
        type (ARunOnAThreadRequiredActionType0Type): For now, this is always `submit_tool_outputs`.
        submit_tool_outputs (ARunOnAThreadRequiredActionType0SubmitToolOutputs): Details on the tool outputs needed for
            this run to continue.
    """

    type: ARunOnAThreadRequiredActionType0Type
    submit_tool_outputs: "ARunOnAThreadRequiredActionType0SubmitToolOutputs"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        submit_tool_outputs = self.submit_tool_outputs.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "submit_tool_outputs": submit_tool_outputs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.a_run_on_a_thread_required_action_type_0_submit_tool_outputs import (
            ARunOnAThreadRequiredActionType0SubmitToolOutputs,
        )

        d = src_dict.copy()
        type = ARunOnAThreadRequiredActionType0Type(d.pop("type"))

        submit_tool_outputs = ARunOnAThreadRequiredActionType0SubmitToolOutputs.from_dict(d.pop("submit_tool_outputs"))

        a_run_on_a_thread_required_action_type_0 = cls(
            type=type,
            submit_tool_outputs=submit_tool_outputs,
        )

        a_run_on_a_thread_required_action_type_0.additional_properties = d
        return a_run_on_a_thread_required_action_type_0

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
