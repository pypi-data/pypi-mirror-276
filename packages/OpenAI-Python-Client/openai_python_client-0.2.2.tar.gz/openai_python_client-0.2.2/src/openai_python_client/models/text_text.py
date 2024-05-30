from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.file_citation import FileCitation
    from ..models.file_path import FilePath


T = TypeVar("T", bound="TextText")


@_attrs_define
class TextText:
    """
    Attributes:
        value (str): The data that makes up the text.
        annotations (List[Union['FileCitation', 'FilePath']]):
    """

    value: str
    annotations: List[Union["FileCitation", "FilePath"]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.file_citation import FileCitation

        value = self.value

        annotations = []
        for annotations_item_data in self.annotations:
            annotations_item: Dict[str, Any]
            if isinstance(annotations_item_data, FileCitation):
                annotations_item = annotations_item_data.to_dict()
            else:
                annotations_item = annotations_item_data.to_dict()

            annotations.append(annotations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "annotations": annotations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_citation import FileCitation
        from ..models.file_path import FilePath

        d = src_dict.copy()
        value = d.pop("value")

        annotations = []
        _annotations = d.pop("annotations")
        for annotations_item_data in _annotations:

            def _parse_annotations_item(data: object) -> Union["FileCitation", "FilePath"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    annotations_item_type_0 = FileCitation.from_dict(data)

                    return annotations_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                annotations_item_type_1 = FilePath.from_dict(data)

                return annotations_item_type_1

            annotations_item = _parse_annotations_item(annotations_item_data)

            annotations.append(annotations_item)

        text_text = cls(
            value=value,
            annotations=annotations,
        )

        text_text.additional_properties = d
        return text_text

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
