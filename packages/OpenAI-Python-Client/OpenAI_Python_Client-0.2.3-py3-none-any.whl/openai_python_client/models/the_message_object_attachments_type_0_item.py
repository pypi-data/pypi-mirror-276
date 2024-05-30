from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.code_interpreter_tool import CodeInterpreterTool
    from ..models.file_search_tool import FileSearchTool


T = TypeVar("T", bound="TheMessageObjectAttachmentsType0Item")


@_attrs_define
class TheMessageObjectAttachmentsType0Item:
    """
    Attributes:
        file_id (Union[Unset, str]): The ID of the file to attach to the message.
        tools (Union[Unset, List[Union['CodeInterpreterTool', 'FileSearchTool']]]): The tools to add this file to.
    """

    file_id: Union[Unset, str] = UNSET
    tools: Union[Unset, List[Union["CodeInterpreterTool", "FileSearchTool"]]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.code_interpreter_tool import CodeInterpreterTool

        file_id = self.file_id

        tools: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item: Dict[str, Any]
                if isinstance(tools_item_data, CodeInterpreterTool):
                    tools_item = tools_item_data.to_dict()
                else:
                    tools_item = tools_item_data.to_dict()

                tools.append(tools_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if file_id is not UNSET:
            field_dict["file_id"] = file_id
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.file_search_tool import FileSearchTool

        d = src_dict.copy()
        file_id = d.pop("file_id", UNSET)

        tools = []
        _tools = d.pop("tools", UNSET)
        for tools_item_data in _tools or []:

            def _parse_tools_item(data: object) -> Union["CodeInterpreterTool", "FileSearchTool"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    tools_item_type_0 = CodeInterpreterTool.from_dict(data)

                    return tools_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                tools_item_type_1 = FileSearchTool.from_dict(data)

                return tools_item_type_1

            tools_item = _parse_tools_item(tools_item_data)

            tools.append(tools_item)

        the_message_object_attachments_type_0_item = cls(
            file_id=file_id,
            tools=tools,
        )

        the_message_object_attachments_type_0_item.additional_properties = d
        return the_message_object_attachments_type_0_item

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
