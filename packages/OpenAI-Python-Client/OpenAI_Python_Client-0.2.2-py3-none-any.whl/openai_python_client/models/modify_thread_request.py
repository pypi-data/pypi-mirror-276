from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modify_thread_request_metadata_type_0 import ModifyThreadRequestMetadataType0
    from ..models.modify_thread_request_tool_resources_type_0 import ModifyThreadRequestToolResourcesType0


T = TypeVar("T", bound="ModifyThreadRequest")


@_attrs_define
class ModifyThreadRequest:
    """
    Attributes:
        tool_resources (Union['ModifyThreadRequestToolResourcesType0', None, Unset]): A set of resources that are made
            available to the assistant's tools in this thread. The resources are specific to the type of tool. For example,
            the `code_interpreter` tool requires a list of file IDs, while the `file_search` tool requires a list of vector
            store IDs.
        metadata (Union['ModifyThreadRequestMetadataType0', None, Unset]): Set of 16 key-value pairs that can be
            attached to an object. This can be useful for storing additional information about the object in a structured
            format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
    """

    tool_resources: Union["ModifyThreadRequestToolResourcesType0", None, Unset] = UNSET
    metadata: Union["ModifyThreadRequestMetadataType0", None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.modify_thread_request_metadata_type_0 import ModifyThreadRequestMetadataType0
        from ..models.modify_thread_request_tool_resources_type_0 import ModifyThreadRequestToolResourcesType0

        tool_resources: Union[Dict[str, Any], None, Unset]
        if isinstance(self.tool_resources, Unset):
            tool_resources = UNSET
        elif isinstance(self.tool_resources, ModifyThreadRequestToolResourcesType0):
            tool_resources = self.tool_resources.to_dict()
        else:
            tool_resources = self.tool_resources

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ModifyThreadRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if tool_resources is not UNSET:
            field_dict["tool_resources"] = tool_resources
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.modify_thread_request_metadata_type_0 import ModifyThreadRequestMetadataType0
        from ..models.modify_thread_request_tool_resources_type_0 import ModifyThreadRequestToolResourcesType0

        d = src_dict.copy()

        def _parse_tool_resources(data: object) -> Union["ModifyThreadRequestToolResourcesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_resources_type_0 = ModifyThreadRequestToolResourcesType0.from_dict(data)

                return tool_resources_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ModifyThreadRequestToolResourcesType0", None, Unset], data)

        tool_resources = _parse_tool_resources(d.pop("tool_resources", UNSET))

        def _parse_metadata(data: object) -> Union["ModifyThreadRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ModifyThreadRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ModifyThreadRequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        modify_thread_request = cls(
            tool_resources=tool_resources,
            metadata=metadata,
        )

        return modify_thread_request
