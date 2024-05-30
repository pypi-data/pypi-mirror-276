from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.text_type import TextType

if TYPE_CHECKING:
    from ..models.text_text import TextText


T = TypeVar("T", bound="Text")


@_attrs_define
class Text:
    """The text content that is part of a message.

    Attributes:
        type (TextType): Always `text`.
        text (TextText):
    """

    type: TextType
    text: "TextText"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        text = self.text.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.text_text import TextText

        d = src_dict.copy()
        type = TextType(d.pop("type"))

        text = TextText.from_dict(d.pop("text"))

        text = cls(
            type=type,
            text=text,
        )

        text.additional_properties = d
        return text

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
