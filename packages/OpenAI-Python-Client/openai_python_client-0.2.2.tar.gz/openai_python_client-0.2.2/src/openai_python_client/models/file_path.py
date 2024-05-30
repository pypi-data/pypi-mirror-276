from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_path_type import FilePathType

if TYPE_CHECKING:
    from ..models.file_path_file_path import FilePathFilePath


T = TypeVar("T", bound="FilePath")


@_attrs_define
class FilePath:
    """A URL for the file that's generated when the assistant used the `code_interpreter` tool to generate a file.

    Attributes:
        type (FilePathType): Always `file_path`.
        text (str): The text in the message content that needs to be replaced.
        file_path (FilePathFilePath):
        start_index (int):
        end_index (int):
    """

    type: FilePathType
    text: str
    file_path: "FilePathFilePath"
    start_index: int
    end_index: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        text = self.text

        file_path = self.file_path.to_dict()

        start_index = self.start_index

        end_index = self.end_index

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "text": text,
                "file_path": file_path,
                "start_index": start_index,
                "end_index": end_index,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_path_file_path import FilePathFilePath

        d = src_dict.copy()
        type = FilePathType(d.pop("type"))

        text = d.pop("text")

        file_path = FilePathFilePath.from_dict(d.pop("file_path"))

        start_index = d.pop("start_index")

        end_index = d.pop("end_index")

        file_path = cls(
            type=type,
            text=text,
            file_path=file_path,
            start_index=start_index,
            end_index=end_index,
        )

        file_path.additional_properties = d
        return file_path

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
