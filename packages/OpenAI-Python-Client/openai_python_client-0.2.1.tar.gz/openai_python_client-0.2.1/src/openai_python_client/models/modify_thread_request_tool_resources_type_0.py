from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modify_thread_request_tool_resources_type_0_code_interpreter import (
        ModifyThreadRequestToolResourcesType0CodeInterpreter,
    )
    from ..models.modify_thread_request_tool_resources_type_0_file_search import (
        ModifyThreadRequestToolResourcesType0FileSearch,
    )


T = TypeVar("T", bound="ModifyThreadRequestToolResourcesType0")


@_attrs_define
class ModifyThreadRequestToolResourcesType0:
    """A set of resources that are made available to the assistant's tools in this thread. The resources are specific to
    the type of tool. For example, the `code_interpreter` tool requires a list of file IDs, while the `file_search` tool
    requires a list of vector store IDs.

        Attributes:
            code_interpreter (Union[Unset, ModifyThreadRequestToolResourcesType0CodeInterpreter]):
            file_search (Union[Unset, ModifyThreadRequestToolResourcesType0FileSearch]):
    """

    code_interpreter: Union[Unset, "ModifyThreadRequestToolResourcesType0CodeInterpreter"] = UNSET
    file_search: Union[Unset, "ModifyThreadRequestToolResourcesType0FileSearch"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code_interpreter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.code_interpreter, Unset):
            code_interpreter = self.code_interpreter.to_dict()

        file_search: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.file_search, Unset):
            file_search = self.file_search.to_dict()

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
        from ..models.modify_thread_request_tool_resources_type_0_code_interpreter import (
            ModifyThreadRequestToolResourcesType0CodeInterpreter,
        )
        from ..models.modify_thread_request_tool_resources_type_0_file_search import (
            ModifyThreadRequestToolResourcesType0FileSearch,
        )

        d = src_dict.copy()
        _code_interpreter = d.pop("code_interpreter", UNSET)
        code_interpreter: Union[Unset, ModifyThreadRequestToolResourcesType0CodeInterpreter]
        if isinstance(_code_interpreter, Unset):
            code_interpreter = UNSET
        else:
            code_interpreter = ModifyThreadRequestToolResourcesType0CodeInterpreter.from_dict(_code_interpreter)

        _file_search = d.pop("file_search", UNSET)
        file_search: Union[Unset, ModifyThreadRequestToolResourcesType0FileSearch]
        if isinstance(_file_search, Unset):
            file_search = UNSET
        else:
            file_search = ModifyThreadRequestToolResourcesType0FileSearch.from_dict(_file_search)

        modify_thread_request_tool_resources_type_0 = cls(
            code_interpreter=code_interpreter,
            file_search=file_search,
        )

        modify_thread_request_tool_resources_type_0.additional_properties = d
        return modify_thread_request_tool_resources_type_0

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
