from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_citation_type import FileCitationType

if TYPE_CHECKING:
    from ..models.file_citation_file_citation import FileCitationFileCitation


T = TypeVar("T", bound="FileCitation")


@_attrs_define
class FileCitation:
    """A citation within the message that points to a specific quote from a specific File associated with the assistant or
    the message. Generated when the assistant uses the "file_search" tool to search files.

        Attributes:
            type (FileCitationType): Always `file_citation`.
            text (str): The text in the message content that needs to be replaced.
            file_citation (FileCitationFileCitation):
            start_index (int):
            end_index (int):
    """

    type: FileCitationType
    text: str
    file_citation: "FileCitationFileCitation"
    start_index: int
    end_index: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        text = self.text

        file_citation = self.file_citation.to_dict()

        start_index = self.start_index

        end_index = self.end_index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "text": text,
                "file_citation": file_citation,
                "start_index": start_index,
                "end_index": end_index,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_citation_file_citation import FileCitationFileCitation

        d = src_dict.copy()
        type = FileCitationType(d.pop("type"))

        text = d.pop("text")

        file_citation = FileCitationFileCitation.from_dict(d.pop("file_citation"))

        start_index = d.pop("start_index")

        end_index = d.pop("end_index")

        file_citation = cls(
            type=type,
            text=text,
            file_citation=file_citation,
            start_index=start_index,
            end_index=end_index,
        )

        file_citation.additional_properties = d
        return file_citation

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
