from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.code_interpreter_log_output_type import CodeInterpreterLogOutputType

T = TypeVar("T", bound="CodeInterpreterLogOutput")


@_attrs_define
class CodeInterpreterLogOutput:
    """Text output from the Code Interpreter tool call as part of a run step.

    Attributes:
        type (CodeInterpreterLogOutputType): Always `logs`.
        logs (str): The text output from the Code Interpreter tool call.
    """

    type: CodeInterpreterLogOutputType
    logs: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        logs = self.logs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "logs": logs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = CodeInterpreterLogOutputType(d.pop("type"))

        logs = d.pop("logs")

        code_interpreter_log_output = cls(
            type=type,
            logs=logs,
        )

        code_interpreter_log_output.additional_properties = d
        return code_interpreter_log_output

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
