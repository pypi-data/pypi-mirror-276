from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.code_interpreter_image_output import CodeInterpreterImageOutput
    from ..models.code_interpreter_log_output import CodeInterpreterLogOutput


T = TypeVar("T", bound="CodeInterpreterToolCallCodeInterpreter")


@_attrs_define
class CodeInterpreterToolCallCodeInterpreter:
    """The Code Interpreter tool call definition.

    Attributes:
        input_ (str): The input to the Code Interpreter tool call.
        outputs (List[Union['CodeInterpreterImageOutput', 'CodeInterpreterLogOutput']]): The outputs from the Code
            Interpreter tool call. Code Interpreter can output one or more items, including text (`logs`) or images
            (`image`). Each of these are represented by a different object type.
    """

    input_: str
    outputs: List[Union["CodeInterpreterImageOutput", "CodeInterpreterLogOutput"]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.code_interpreter_log_output import CodeInterpreterLogOutput

        input_ = self.input_

        outputs = []
        for outputs_item_data in self.outputs:
            outputs_item: Dict[str, Any]
            if isinstance(outputs_item_data, CodeInterpreterLogOutput):
                outputs_item = outputs_item_data.to_dict()
            else:
                outputs_item = outputs_item_data.to_dict()

            outputs.append(outputs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
                "outputs": outputs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.code_interpreter_image_output import CodeInterpreterImageOutput
        from ..models.code_interpreter_log_output import CodeInterpreterLogOutput

        d = src_dict.copy()
        input_ = d.pop("input")

        outputs = []
        _outputs = d.pop("outputs")
        for outputs_item_data in _outputs:

            def _parse_outputs_item(data: object) -> Union["CodeInterpreterImageOutput", "CodeInterpreterLogOutput"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    outputs_item_type_0 = CodeInterpreterLogOutput.from_dict(data)

                    return outputs_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                outputs_item_type_1 = CodeInterpreterImageOutput.from_dict(data)

                return outputs_item_type_1

            outputs_item = _parse_outputs_item(outputs_item_data)

            outputs.append(outputs_item)

        code_interpreter_tool_call_code_interpreter = cls(
            input_=input_,
            outputs=outputs,
        )

        code_interpreter_tool_call_code_interpreter.additional_properties = d
        return code_interpreter_tool_call_code_interpreter

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
