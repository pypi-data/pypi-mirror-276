from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.code_interpreter_image_output_type import CodeInterpreterImageOutputType

if TYPE_CHECKING:
    from ..models.code_interpreter_image_output_image import CodeInterpreterImageOutputImage


T = TypeVar("T", bound="CodeInterpreterImageOutput")


@_attrs_define
class CodeInterpreterImageOutput:
    """
    Attributes:
        type (CodeInterpreterImageOutputType): Always `image`.
        image (CodeInterpreterImageOutputImage):
    """

    type: CodeInterpreterImageOutputType
    image: "CodeInterpreterImageOutputImage"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        image = self.image.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "image": image,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.code_interpreter_image_output_image import CodeInterpreterImageOutputImage

        d = src_dict.copy()
        type = CodeInterpreterImageOutputType(d.pop("type"))

        image = CodeInterpreterImageOutputImage.from_dict(d.pop("image"))

        code_interpreter_image_output = cls(
            type=type,
            image=image,
        )

        code_interpreter_image_output.additional_properties = d
        return code_interpreter_image_output

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
