from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_search_tool_call_type import FileSearchToolCallType

if TYPE_CHECKING:
    from ..models.file_search_tool_call_file_search import FileSearchToolCallFileSearch


T = TypeVar("T", bound="FileSearchToolCall")


@_attrs_define
class FileSearchToolCall:
    """
    Attributes:
        id (str): The ID of the tool call object.
        type (FileSearchToolCallType): The type of tool call. This is always going to be `file_search` for this type of
            tool call.
        file_search (FileSearchToolCallFileSearch): For now, this is always going to be an empty object.
    """

    id: str
    type: FileSearchToolCallType
    file_search: "FileSearchToolCallFileSearch"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        type = self.type.value

        file_search = self.file_search.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "file_search": file_search,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_search_tool_call_file_search import FileSearchToolCallFileSearch

        d = src_dict.copy()
        id = d.pop("id")

        type = FileSearchToolCallType(d.pop("type"))

        file_search = FileSearchToolCallFileSearch.from_dict(d.pop("file_search"))

        file_search_tool_call = cls(
            id=id,
            type=type,
            file_search=file_search,
        )

        file_search_tool_call.additional_properties = d
        return file_search_tool_call

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
