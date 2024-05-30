from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tool_calls_type import ToolCallsType

if TYPE_CHECKING:
    from ..models.code_interpreter_tool_call import CodeInterpreterToolCall
    from ..models.file_search_tool_call import FileSearchToolCall
    from ..models.function_tool_call import FunctionToolCall


T = TypeVar("T", bound="ToolCalls")


@_attrs_define
class ToolCalls:
    """Details of the tool call.

    Attributes:
        type (ToolCallsType): Always `tool_calls`.
        tool_calls (List[Union['CodeInterpreterToolCall', 'FileSearchToolCall', 'FunctionToolCall']]): An array of tool
            calls the run step was involved in. These can be associated with one of three types of tools:
            `code_interpreter`, `file_search`, or `function`.
    """

    type: ToolCallsType
    tool_calls: List[Union["CodeInterpreterToolCall", "FileSearchToolCall", "FunctionToolCall"]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.code_interpreter_tool_call import CodeInterpreterToolCall
        from ..models.file_search_tool_call import FileSearchToolCall

        type = self.type.value

        tool_calls = []
        for tool_calls_item_data in self.tool_calls:
            tool_calls_item: Dict[str, Any]
            if isinstance(tool_calls_item_data, CodeInterpreterToolCall):
                tool_calls_item = tool_calls_item_data.to_dict()
            elif isinstance(tool_calls_item_data, FileSearchToolCall):
                tool_calls_item = tool_calls_item_data.to_dict()
            else:
                tool_calls_item = tool_calls_item_data.to_dict()

            tool_calls.append(tool_calls_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "tool_calls": tool_calls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.code_interpreter_tool_call import CodeInterpreterToolCall
        from ..models.file_search_tool_call import FileSearchToolCall
        from ..models.function_tool_call import FunctionToolCall

        d = src_dict.copy()
        type = ToolCallsType(d.pop("type"))

        tool_calls = []
        _tool_calls = d.pop("tool_calls")
        for tool_calls_item_data in _tool_calls:

            def _parse_tool_calls_item(
                data: object,
            ) -> Union["CodeInterpreterToolCall", "FileSearchToolCall", "FunctionToolCall"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    tool_calls_item_type_0 = CodeInterpreterToolCall.from_dict(data)

                    return tool_calls_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    tool_calls_item_type_1 = FileSearchToolCall.from_dict(data)

                    return tool_calls_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                tool_calls_item_type_2 = FunctionToolCall.from_dict(data)

                return tool_calls_item_type_2

            tool_calls_item = _parse_tool_calls_item(tool_calls_item_data)

            tool_calls.append(tool_calls_item)

        tool_calls = cls(
            type=type,
            tool_calls=tool_calls,
        )

        tool_calls.additional_properties = d
        return tool_calls

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
