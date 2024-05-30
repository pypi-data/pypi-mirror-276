from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_message_request import CreateMessageRequest
    from ..models.create_thread_request_metadata_type_0 import CreateThreadRequestMetadataType0
    from ..models.create_thread_request_tool_resources_type_0 import CreateThreadRequestToolResourcesType0


T = TypeVar("T", bound="CreateThreadRequest")


@_attrs_define
class CreateThreadRequest:
    """
    Attributes:
        messages (Union[Unset, List['CreateMessageRequest']]): A list of [messages](/docs/api-reference/messages) to
            start the thread with.
        tool_resources (Union['CreateThreadRequestToolResourcesType0', None, Unset]): A set of resources that are made
            available to the assistant's tools in this thread. The resources are specific to the type of tool. For example,
            the `code_interpreter` tool requires a list of file IDs, while the `file_search` tool requires a list of vector
            store IDs.
        metadata (Union['CreateThreadRequestMetadataType0', None, Unset]): Set of 16 key-value pairs that can be
            attached to an object. This can be useful for storing additional information about the object in a structured
            format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
    """

    messages: Union[Unset, List["CreateMessageRequest"]] = UNSET
    tool_resources: Union["CreateThreadRequestToolResourcesType0", None, Unset] = UNSET
    metadata: Union["CreateThreadRequestMetadataType0", None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.create_thread_request_metadata_type_0 import CreateThreadRequestMetadataType0
        from ..models.create_thread_request_tool_resources_type_0 import CreateThreadRequestToolResourcesType0

        messages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.messages, Unset):
            messages = []
            for messages_item_data in self.messages:
                messages_item = messages_item_data.to_dict()
                messages.append(messages_item)

        tool_resources: Union[Dict[str, Any], None, Unset]
        if isinstance(self.tool_resources, Unset):
            tool_resources = UNSET
        elif isinstance(self.tool_resources, CreateThreadRequestToolResourcesType0):
            tool_resources = self.tool_resources.to_dict()
        else:
            tool_resources = self.tool_resources

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, CreateThreadRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if messages is not UNSET:
            field_dict["messages"] = messages
        if tool_resources is not UNSET:
            field_dict["tool_resources"] = tool_resources
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_message_request import CreateMessageRequest
        from ..models.create_thread_request_metadata_type_0 import CreateThreadRequestMetadataType0
        from ..models.create_thread_request_tool_resources_type_0 import CreateThreadRequestToolResourcesType0

        d = src_dict.copy()
        messages = []
        _messages = d.pop("messages", UNSET)
        for messages_item_data in _messages or []:
            messages_item = CreateMessageRequest.from_dict(messages_item_data)

            messages.append(messages_item)

        def _parse_tool_resources(data: object) -> Union["CreateThreadRequestToolResourcesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_resources_type_0 = CreateThreadRequestToolResourcesType0.from_dict(data)

                return tool_resources_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateThreadRequestToolResourcesType0", None, Unset], data)

        tool_resources = _parse_tool_resources(d.pop("tool_resources", UNSET))

        def _parse_metadata(data: object) -> Union["CreateThreadRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = CreateThreadRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateThreadRequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        create_thread_request = cls(
            messages=messages,
            tool_resources=tool_resources,
            metadata=metadata,
        )

        return create_thread_request
