from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.image_content_part_image_url_detail import ImageContentPartImageUrlDetail
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageContentPartImageUrl")


@_attrs_define
class ImageContentPartImageUrl:
    """
    Attributes:
        url (str): Either a URL of the image or the base64 encoded image data.
        detail (Union[Unset, ImageContentPartImageUrlDetail]): Specifies the detail level of the image. Learn more in
            the [Vision guide](/docs/guides/vision/low-or-high-fidelity-image-understanding). Default:
            ImageContentPartImageUrlDetail.AUTO.
    """

    url: str
    detail: Union[Unset, ImageContentPartImageUrlDetail] = ImageContentPartImageUrlDetail.AUTO
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url

        detail: Union[Unset, str] = UNSET
        if not isinstance(self.detail, Unset):
            detail = self.detail.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        _detail = d.pop("detail", UNSET)
        detail: Union[Unset, ImageContentPartImageUrlDetail]
        if isinstance(_detail, Unset):
            detail = UNSET
        else:
            detail = ImageContentPartImageUrlDetail(_detail)

        image_content_part_image_url = cls(
            url=url,
            detail=detail,
        )

        image_content_part_image_url.additional_properties = d
        return image_content_part_image_url

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
