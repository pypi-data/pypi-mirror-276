from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transcription_segment import TranscriptionSegment
    from ..models.transcription_word import TranscriptionWord


T = TypeVar("T", bound="CreateTranscriptionResponseVerboseJson")


@_attrs_define
class CreateTranscriptionResponseVerboseJson:
    """Represents a verbose json transcription response returned by model, based on the provided input.

    Attributes:
        language (str): The language of the input audio.
        duration (str): The duration of the input audio.
        text (str): The transcribed text.
        words (Union[Unset, List['TranscriptionWord']]): Extracted words and their corresponding timestamps.
        segments (Union[Unset, List['TranscriptionSegment']]): Segments of the transcribed text and their corresponding
            details.
    """

    language: str
    duration: str
    text: str
    words: Union[Unset, List["TranscriptionWord"]] = UNSET
    segments: Union[Unset, List["TranscriptionSegment"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        language = self.language

        duration = self.duration

        text = self.text

        words: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.words, Unset):
            words = []
            for words_item_data in self.words:
                words_item = words_item_data.to_dict()
                words.append(words_item)

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
        if words is not UNSET:
            field_dict["words"] = words
        if segments is not UNSET:
            field_dict["segments"] = segments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.transcription_segment import TranscriptionSegment
        from ..models.transcription_word import TranscriptionWord

        d = src_dict.copy()
        language = d.pop("language")

        duration = d.pop("duration")

        text = d.pop("text")

        words = []
        _words = d.pop("words", UNSET)
        for words_item_data in _words or []:
            words_item = TranscriptionWord.from_dict(words_item_data)

            words.append(words_item)

        segments = []
        _segments = d.pop("segments", UNSET)
        for segments_item_data in _segments or []:
            segments_item = TranscriptionSegment.from_dict(segments_item_data)

            segments.append(segments_item)

        create_transcription_response_verbose_json = cls(
            language=language,
            duration=duration,
            text=text,
            words=words,
            segments=segments,
        )

        create_transcription_response_verbose_json.additional_properties = d
        return create_transcription_response_verbose_json

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
