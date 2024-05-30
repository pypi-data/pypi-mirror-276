from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.the_message_object_object import TheMessageObjectObject
from ..models.the_message_object_role import TheMessageObjectRole
from ..models.the_message_object_status import TheMessageObjectStatus

if TYPE_CHECKING:
    from ..models.image_file import ImageFile
    from ..models.text import Text
    from ..models.the_message_object_attachments_type_0_item import TheMessageObjectAttachmentsType0Item
    from ..models.the_message_object_incomplete_details_type_0 import TheMessageObjectIncompleteDetailsType0
    from ..models.the_message_object_metadata_type_0 import TheMessageObjectMetadataType0


T = TypeVar("T", bound="TheMessageObject")


@_attrs_define
class TheMessageObject:
    """Represents a message within a [thread](/docs/api-reference/threads).

    Attributes:
        id (str): The identifier, which can be referenced in API endpoints.
        object_ (TheMessageObjectObject): The object type, which is always `thread.message`.
        created_at (int): The Unix timestamp (in seconds) for when the message was created.
        thread_id (str): The [thread](/docs/api-reference/threads) ID that this message belongs to.
        status (TheMessageObjectStatus): The status of the message, which can be either `in_progress`, `incomplete`, or
            `completed`.
        incomplete_details (Union['TheMessageObjectIncompleteDetailsType0', None]): On an incomplete message, details
            about why the message is incomplete.
        completed_at (Union[None, int]): The Unix timestamp (in seconds) for when the message was completed.
        incomplete_at (Union[None, int]): The Unix timestamp (in seconds) for when the message was marked as incomplete.
        role (TheMessageObjectRole): The entity that produced the message. One of `user` or `assistant`.
        content (List[Union['ImageFile', 'Text']]): The content of the message in array of text and/or images.
        assistant_id (Union[None, str]): If applicable, the ID of the [assistant](/docs/api-reference/assistants) that
            authored this message.
        run_id (Union[None, str]): The ID of the [run](/docs/api-reference/runs) associated with the creation of this
            message. Value is `null` when messages are created manually using the create message or create thread endpoints.
        attachments (Union[List['TheMessageObjectAttachmentsType0Item'], None]): A list of files attached to the
            message, and the tools they were added to.
        metadata (Union['TheMessageObjectMetadataType0', None]): Set of 16 key-value pairs that can be attached to an
            object. This can be useful for storing additional information about the object in a structured format. Keys can
            be a maximum of 64 characters long and values can be a maxium of 512 characters long.
    """

    id: str
    object_: TheMessageObjectObject
    created_at: int
    thread_id: str
    status: TheMessageObjectStatus
    incomplete_details: Union["TheMessageObjectIncompleteDetailsType0", None]
    completed_at: Union[None, int]
    incomplete_at: Union[None, int]
    role: TheMessageObjectRole
    content: List[Union["ImageFile", "Text"]]
    assistant_id: Union[None, str]
    run_id: Union[None, str]
    attachments: Union[List["TheMessageObjectAttachmentsType0Item"], None]
    metadata: Union["TheMessageObjectMetadataType0", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.image_file import ImageFile
        from ..models.the_message_object_incomplete_details_type_0 import TheMessageObjectIncompleteDetailsType0
        from ..models.the_message_object_metadata_type_0 import TheMessageObjectMetadataType0

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at

        thread_id = self.thread_id

        status = self.status.value

        incomplete_details: Union[Dict[str, Any], None]
        if isinstance(self.incomplete_details, TheMessageObjectIncompleteDetailsType0):
            incomplete_details = self.incomplete_details.to_dict()
        else:
            incomplete_details = self.incomplete_details

        completed_at: Union[None, int]
        completed_at = self.completed_at

        incomplete_at: Union[None, int]
        incomplete_at = self.incomplete_at

        role = self.role.value

        content = []
        for content_item_data in self.content:
            content_item: Dict[str, Any]
            if isinstance(content_item_data, ImageFile):
                content_item = content_item_data.to_dict()
            else:
                content_item = content_item_data.to_dict()

            content.append(content_item)

        assistant_id: Union[None, str]
        assistant_id = self.assistant_id

        run_id: Union[None, str]
        run_id = self.run_id

        attachments: Union[List[Dict[str, Any]], None]
        if isinstance(self.attachments, list):
            attachments = []
            for attachments_type_0_item_data in self.attachments:
                attachments_type_0_item = attachments_type_0_item_data.to_dict()
                attachments.append(attachments_type_0_item)

        else:
            attachments = self.attachments

        metadata: Union[Dict[str, Any], None]
        if isinstance(self.metadata, TheMessageObjectMetadataType0):
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
                "thread_id": thread_id,
                "status": status,
                "incomplete_details": incomplete_details,
                "completed_at": completed_at,
                "incomplete_at": incomplete_at,
                "role": role,
                "content": content,
                "assistant_id": assistant_id,
                "run_id": run_id,
                "attachments": attachments,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.image_file import ImageFile
        from ..models.text import Text
        from ..models.the_message_object_attachments_type_0_item import TheMessageObjectAttachmentsType0Item
        from ..models.the_message_object_incomplete_details_type_0 import TheMessageObjectIncompleteDetailsType0
        from ..models.the_message_object_metadata_type_0 import TheMessageObjectMetadataType0

        d = src_dict.copy()
        id = d.pop("id")

        object_ = TheMessageObjectObject(d.pop("object"))

        created_at = d.pop("created_at")

        thread_id = d.pop("thread_id")

        status = TheMessageObjectStatus(d.pop("status"))

        def _parse_incomplete_details(data: object) -> Union["TheMessageObjectIncompleteDetailsType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                incomplete_details_type_0 = TheMessageObjectIncompleteDetailsType0.from_dict(data)

                return incomplete_details_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TheMessageObjectIncompleteDetailsType0", None], data)

        incomplete_details = _parse_incomplete_details(d.pop("incomplete_details"))

        def _parse_completed_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        def _parse_incomplete_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        incomplete_at = _parse_incomplete_at(d.pop("incomplete_at"))

        role = TheMessageObjectRole(d.pop("role"))

        content = []
        _content = d.pop("content")
        for content_item_data in _content:

            def _parse_content_item(data: object) -> Union["ImageFile", "Text"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    content_item_type_0 = ImageFile.from_dict(data)

                    return content_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                content_item_type_1 = Text.from_dict(data)

                return content_item_type_1

            content_item = _parse_content_item(content_item_data)

            content.append(content_item)

        def _parse_assistant_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        assistant_id = _parse_assistant_id(d.pop("assistant_id"))

        def _parse_run_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        run_id = _parse_run_id(d.pop("run_id"))

        def _parse_attachments(data: object) -> Union[List["TheMessageObjectAttachmentsType0Item"], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                attachments_type_0 = []
                _attachments_type_0 = data
                for attachments_type_0_item_data in _attachments_type_0:
                    attachments_type_0_item = TheMessageObjectAttachmentsType0Item.from_dict(
                        attachments_type_0_item_data
                    )

                    attachments_type_0.append(attachments_type_0_item)

                return attachments_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["TheMessageObjectAttachmentsType0Item"], None], data)

        attachments = _parse_attachments(d.pop("attachments"))

        def _parse_metadata(data: object) -> Union["TheMessageObjectMetadataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = TheMessageObjectMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TheMessageObjectMetadataType0", None], data)

        metadata = _parse_metadata(d.pop("metadata"))

        the_message_object = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            thread_id=thread_id,
            status=status,
            incomplete_details=incomplete_details,
            completed_at=completed_at,
            incomplete_at=incomplete_at,
            role=role,
            content=content,
            assistant_id=assistant_id,
            run_id=run_id,
            attachments=attachments,
            metadata=metadata,
        )

        the_message_object.additional_properties = d
        return the_message_object

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
