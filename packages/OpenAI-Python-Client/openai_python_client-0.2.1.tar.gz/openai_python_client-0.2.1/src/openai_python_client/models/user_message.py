from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_message_role import UserMessageRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_content_part import ImageContentPart
    from ..models.text_content_part import TextContentPart


T = TypeVar("T", bound="UserMessage")


@_attrs_define
class UserMessage:
    """
    Attributes:
        content (Union[List[Union['ImageContentPart', 'TextContentPart']], str]): The contents of the user message.
        role (UserMessageRole): The role of the messages author, in this case `user`.
        name (Union[Unset, str]): An optional name for the participant. Provides the model information to differentiate
            between participants of the same role.
    """

    content: Union[List[Union["ImageContentPart", "TextContentPart"]], str]
    role: UserMessageRole
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.text_content_part import TextContentPart

        content: Union[List[Dict[str, Any]], str]
        if isinstance(self.content, list):
            content = []
            for content_type_1_item_data in self.content:
                content_type_1_item: Dict[str, Any]
                if isinstance(content_type_1_item_data, TextContentPart):
                    content_type_1_item = content_type_1_item_data.to_dict()
                else:
                    content_type_1_item = content_type_1_item_data.to_dict()

                content.append(content_type_1_item)

        else:
            content = self.content

        role = self.role.value

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "role": role,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.image_content_part import ImageContentPart
        from ..models.text_content_part import TextContentPart

        d = src_dict.copy()

        def _parse_content(data: object) -> Union[List[Union["ImageContentPart", "TextContentPart"]], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_1 = []
                _content_type_1 = data
                for content_type_1_item_data in _content_type_1:

                    def _parse_content_type_1_item(data: object) -> Union["ImageContentPart", "TextContentPart"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemas_chat_completion_request_message_content_part_type_0 = (
                                TextContentPart.from_dict(data)
                            )

                            return componentsschemas_chat_completion_request_message_content_part_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_chat_completion_request_message_content_part_type_1 = (
                            ImageContentPart.from_dict(data)
                        )

                        return componentsschemas_chat_completion_request_message_content_part_type_1

                    content_type_1_item = _parse_content_type_1_item(content_type_1_item_data)

                    content_type_1.append(content_type_1_item)

                return content_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[Union["ImageContentPart", "TextContentPart"]], str], data)

        content = _parse_content(d.pop("content"))

        role = UserMessageRole(d.pop("role"))

        name = d.pop("name", UNSET)

        user_message = cls(
            content=content,
            role=role,
            name=name,
        )

        user_message.additional_properties = d
        return user_message

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
