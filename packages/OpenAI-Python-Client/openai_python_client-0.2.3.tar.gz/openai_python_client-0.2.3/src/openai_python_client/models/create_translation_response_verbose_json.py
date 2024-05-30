from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transcription_segment import TranscriptionSegment


T = TypeVar("T", bound="CreateTranslationResponseVerboseJson")


@_attrs_define
class CreateTranslationResponseVerboseJson:
    """
    Attributes:
        language (str): The language of the output translation (always `english`).
        duration (str): The duration of the input audio.
        text (str): The translated text.
        segments (Union[Unset, List['TranscriptionSegment']]): Segments of the translated text and their corresponding
            details.
    """

    language: str
    duration: str
    text: str
    segments: Union[Unset, List["TranscriptionSegment"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        language = self.language

        duration = self.duration

        text = self.text

        segments: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.segments, Unset):
            segments = []
            for segments_item_data in self.segments:
                segments_item = segments_item_data.to_dict()
                segments.append(segments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "language": language,
                "duration": duration,
                "text": text,
            }
        )
        if segments is not UNSET:
            field_dict["segments"] = segments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.transcription_segment import TranscriptionSegment

        d = src_dict.copy()
        language = d.pop("language")

        duration = d.pop("duration")

        text = d.pop("text")

        segments = []
        _segments = d.pop("segments", UNSET)
        for segments_item_data in _segments or []:
            segments_item = TranscriptionSegment.from_dict(segments_item_data)

            segments.append(segments_item)

        create_translation_response_verbose_json = cls(
            language=language,
            duration=duration,
            text=text,
            segments=segments,
        )

        create_translation_response_verbose_json.additional_properties = d
        return create_translation_response_verbose_json

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
