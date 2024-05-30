from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TranscriptionWord")


@_attrs_define
class TranscriptionWord:
    """
    Attributes:
        word (str): The text content of the word.
        start (float): Start time of the word in seconds.
        end (float): End time of the word in seconds.
    """

    word: str
    start: float
    end: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        word = self.word

        start = self.start

        end = self.end

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "word": word,
                "start": start,
                "end": end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        word = d.pop("word")

        start = d.pop("start")

        end = d.pop("end")

        transcription_word = cls(
            word=word,
            start=start,
            end=end,
        )

        transcription_word.additional_properties = d
        return transcription_word

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
