from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_assistant_request_tool_resources_type_0_code_interpreter import (
        CreateAssistantRequestToolResourcesType0CodeInterpreter,
    )


T = TypeVar("T", bound="CreateAssistantRequestToolResourcesType0")


@_attrs_define
class CreateAssistantRequestToolResourcesType0:
    """A set of resources that are used by the assistant's tools. The resources are specific to the type of tool. For
    example, the `code_interpreter` tool requires a list of file IDs, while the `file_search` tool requires a list of
    vector store IDs.

        Attributes:
            code_interpreter (Union[Unset, CreateAssistantRequestToolResourcesType0CodeInterpreter]):
            file_search (Union[Any, Unset]):
    """

    code_interpreter: Union[Unset, "CreateAssistantRequestToolResourcesType0CodeInterpreter"] = UNSET
    file_search: Union[Any, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code_interpreter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.code_interpreter, Unset):
            code_interpreter = self.code_interpreter.to_dict()

        file_search: Union[Any, Unset]
        if isinstance(self.file_search, Unset):
            file_search = UNSET
        else:
            file_search = self.file_search

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code_interpreter is not UNSET:
            field_dict["code_interpreter"] = code_interpreter
        if file_search is not UNSET:
            field_dict["file_search"] = file_search

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_assistant_request_tool_resources_type_0_code_interpreter import (
            CreateAssistantRequestToolResourcesType0CodeInterpreter,
        )

        d = src_dict.copy()
        _code_interpreter = d.pop("code_interpreter", UNSET)
        code_interpreter: Union[Unset, CreateAssistantRequestToolResourcesType0CodeInterpreter]
        if isinstance(_code_interpreter, Unset):
            code_interpreter = UNSET
        else:
            code_interpreter = CreateAssistantRequestToolResourcesType0CodeInterpreter.from_dict(_code_interpreter)

        def _parse_file_search(data: object) -> Union[Any, Unset]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset], data)

        file_search = _parse_file_search(d.pop("file_search", UNSET))

        create_assistant_request_tool_resources_type_0 = cls(
            code_interpreter=code_interpreter,
            file_search=file_search,
        )

        create_assistant_request_tool_resources_type_0.additional_properties = d
        return create_assistant_request_tool_resources_type_0

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
