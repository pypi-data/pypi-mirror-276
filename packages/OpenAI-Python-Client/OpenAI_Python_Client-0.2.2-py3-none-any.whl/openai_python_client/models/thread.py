from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.thread_object import ThreadObject

if TYPE_CHECKING:
    from ..models.thread_metadata_type_0 import ThreadMetadataType0
    from ..models.thread_tool_resources_type_0 import ThreadToolResourcesType0


T = TypeVar("T", bound="Thread")


@_attrs_define
class Thread:
    """Represents a thread that contains [messages](/docs/api-reference/messages).

    Attributes:
        id (str): The identifier, which can be referenced in API endpoints.
        object_ (ThreadObject): The object type, which is always `thread`.
        created_at (int): The Unix timestamp (in seconds) for when the thread was created.
        tool_resources (Union['ThreadToolResourcesType0', None]): A set of resources that are made available to the
            assistant's tools in this thread. The resources are specific to the type of tool. For example, the
            `code_interpreter` tool requires a list of file IDs, while the `file_search` tool requires a list of vector
            store IDs.
        metadata (Union['ThreadMetadataType0', None]): Set of 16 key-value pairs that can be attached to an object. This
            can be useful for storing additional information about the object in a structured format. Keys can be a maximum
            of 64 characters long and values can be a maxium of 512 characters long.
    """

    id: str
    object_: ThreadObject
    created_at: int
    tool_resources: Union["ThreadToolResourcesType0", None]
    metadata: Union["ThreadMetadataType0", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.thread_metadata_type_0 import ThreadMetadataType0
        from ..models.thread_tool_resources_type_0 import ThreadToolResourcesType0

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at

        tool_resources: Union[Dict[str, Any], None]
        if isinstance(self.tool_resources, ThreadToolResourcesType0):
            tool_resources = self.tool_resources.to_dict()
        else:
            tool_resources = self.tool_resources

        metadata: Union[Dict[str, Any], None]
        if isinstance(self.metadata, ThreadMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "tool_resources": tool_resources,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.thread_metadata_type_0 import ThreadMetadataType0
        from ..models.thread_tool_resources_type_0 import ThreadToolResourcesType0

        d = src_dict.copy()
        id = d.pop("id")

        object_ = ThreadObject(d.pop("object"))

        created_at = d.pop("created_at")

        def _parse_tool_resources(data: object) -> Union["ThreadToolResourcesType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_resources_type_0 = ThreadToolResourcesType0.from_dict(data)

                return tool_resources_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ThreadToolResourcesType0", None], data)

        tool_resources = _parse_tool_resources(d.pop("tool_resources"))

        def _parse_metadata(data: object) -> Union["ThreadMetadataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ThreadMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ThreadMetadataType0", None], data)

        metadata = _parse_metadata(d.pop("metadata"))

        thread = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            tool_resources=tool_resources,
            metadata=metadata,
        )

        thread.additional_properties = d
        return thread

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
