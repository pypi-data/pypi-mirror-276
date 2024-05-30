import json
from io import BytesIO
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.create_transcription_request_model_type_1 import CreateTranscriptionRequestModelType1
from ..models.create_transcription_request_response_format import CreateTranscriptionRequestResponseFormat
from ..models.create_transcription_request_timestamp_granularities_item import (
    CreateTranscriptionRequestTimestampGranularitiesItem,
)
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="CreateTranscriptionRequest")


@_attrs_define
class CreateTranscriptionRequest:
    """
    Attributes:
        file (File): The audio file object (not file name) to transcribe, in one of these formats: flac, mp3, mp4, mpeg,
            mpga, m4a, ogg, wav, or webm.
        model (Union[CreateTranscriptionRequestModelType1, str]): ID of the model to use. Only `whisper-1` (which is
            powered by our open source Whisper V2 model) is currently available.
             Example: whisper-1.
        language (Union[Unset, str]): The language of the input audio. Supplying the input language in
            [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) format will improve accuracy and latency.
        prompt (Union[Unset, str]): An optional text to guide the model's style or continue a previous audio segment.
            The [prompt](/docs/guides/speech-to-text/prompting) should match the audio language.
        response_format (Union[Unset, CreateTranscriptionRequestResponseFormat]): The format of the transcript output,
            in one of these options: `json`, `text`, `srt`, `verbose_json`, or `vtt`.
             Default: CreateTranscriptionRequestResponseFormat.JSON.
        temperature (Union[Unset, float]): The sampling temperature, between 0 and 1. Higher values like 0.8 will make
            the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0,
            the model will use [log probability](https://en.wikipedia.org/wiki/Log_probability) to automatically increase
            the temperature until certain thresholds are hit.
             Default: 0.0.
        timestamp_granularities (Union[Unset, List[CreateTranscriptionRequestTimestampGranularitiesItem]]): The
            timestamp granularities to populate for this transcription. `response_format` must be set `verbose_json` to use
            timestamp granularities. Either or both of these options are supported: `word`, or `segment`. Note: There is no
            additional latency for segment timestamps, but generating word timestamps incurs additional latency.
    """

    file: File
    model: Union[CreateTranscriptionRequestModelType1, str]
    language: Union[Unset, str] = UNSET
    prompt: Union[Unset, str] = UNSET
    response_format: Union[Unset, CreateTranscriptionRequestResponseFormat] = (
        CreateTranscriptionRequestResponseFormat.JSON
    )
    temperature: Union[Unset, float] = 0.0
    timestamp_granularities: Union[Unset, List[CreateTranscriptionRequestTimestampGranularitiesItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        model: str
        if isinstance(self.model, CreateTranscriptionRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        language = self.language

        prompt = self.prompt

        response_format: Union[Unset, str] = UNSET
        if not isinstance(self.response_format, Unset):
            response_format = self.response_format.value

        temperature = self.temperature

        timestamp_granularities: Union[Unset, List[str]] = UNSET
        if not isinstance(self.timestamp_granularities, Unset):
            timestamp_granularities = []
            for timestamp_granularities_item_data in self.timestamp_granularities:
                timestamp_granularities_item = timestamp_granularities_item_data.value
                timestamp_granularities.append(timestamp_granularities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "file": file,
                "model": model,
            }
        )
        if language is not UNSET:
            field_dict["language"] = language
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if timestamp_granularities is not UNSET:
            field_dict["timestamp_granularities[]"] = timestamp_granularities

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        model: Union[CreateTranscriptionRequestModelType1, str]
        if isinstance(self.model, CreateTranscriptionRequestModelType1):
            model = (None, str(self.model.value).encode(), "text/plain")
        else:
            model = self.model

        language = (
            self.language if isinstance(self.language, Unset) else (None, str(self.language).encode(), "text/plain")
        )

        prompt = self.prompt if isinstance(self.prompt, Unset) else (None, str(self.prompt).encode(), "text/plain")

        response_format: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.response_format, Unset):
            response_format = (None, str(self.response_format.value).encode(), "text/plain")

        temperature = (
            self.temperature
            if isinstance(self.temperature, Unset)
            else (None, str(self.temperature).encode(), "text/plain")
        )

        timestamp_granularities: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.timestamp_granularities, Unset):
            _temp_timestamp_granularities = []
            for timestamp_granularities_item_data in self.timestamp_granularities:
                timestamp_granularities_item = timestamp_granularities_item_data.value
                _temp_timestamp_granularities.append(timestamp_granularities_item)
            timestamp_granularities = (None, json.dumps(_temp_timestamp_granularities).encode(), "application/json")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "file": file,
                "model": model,
            }
        )
        if language is not UNSET:
            field_dict["language"] = language
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if timestamp_granularities is not UNSET:
            field_dict["timestamp_granularities[]"] = timestamp_granularities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file = File(payload=BytesIO(d.pop("file")))

        def _parse_model(data: object) -> Union[CreateTranscriptionRequestModelType1, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateTranscriptionRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateTranscriptionRequestModelType1, str], data)

        model = _parse_model(d.pop("model"))

        language = d.pop("language", UNSET)

        prompt = d.pop("prompt", UNSET)

        _response_format = d.pop("response_format", UNSET)
        response_format: Union[Unset, CreateTranscriptionRequestResponseFormat]
        if isinstance(_response_format, Unset):
            response_format = UNSET
        else:
            response_format = CreateTranscriptionRequestResponseFormat(_response_format)

        temperature = d.pop("temperature", UNSET)

        timestamp_granularities = []
        _timestamp_granularities = d.pop("timestamp_granularities[]", UNSET)
        for timestamp_granularities_item_data in _timestamp_granularities or []:
            timestamp_granularities_item = CreateTranscriptionRequestTimestampGranularitiesItem(
                timestamp_granularities_item_data
            )

            timestamp_granularities.append(timestamp_granularities_item)

        create_transcription_request = cls(
            file=file,
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            timestamp_granularities=timestamp_granularities,
        )

        return create_transcription_request
