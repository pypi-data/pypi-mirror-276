from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.image_content_part_type import ImageContentPartType

if TYPE_CHECKING:
    from ..models.image_content_part_image_url import ImageContentPartImageUrl


T = TypeVar("T", bound="ImageContentPart")


@_attrs_define
class ImageContentPart:
    """
    Attributes:
        type (ImageContentPartType): The type of the content part.
        image_url (ImageContentPartImageUrl):
    """

    type: ImageContentPartType
    image_url: "ImageContentPartImageUrl"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        image_url = self.image_url.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "image_url": image_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.image_content_part_image_url import ImageContentPartImageUrl

        d = src_dict.copy()
        type = ImageContentPartType(d.pop("type"))

        image_url = ImageContentPartImageUrl.from_dict(d.pop("image_url"))

        image_content_part = cls(
            type=type,
            image_url=image_url,
        )

        image_content_part.additional_properties = d
        return image_content_part

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
