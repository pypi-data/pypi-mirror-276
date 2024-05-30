from io import BytesIO
from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.create_translation_request_model_type_1 import CreateTranslationRequestModelType1
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="CreateTranslationRequest")


@_attrs_define
class CreateTranslationRequest:
    """
    Attributes:
        file (File): The audio file object (not file name) translate, in one of these formats: flac, mp3, mp4, mpeg,
            mpga, m4a, ogg, wav, or webm.
        model (Union[CreateTranslationRequestModelType1, str]): ID of the model to use. Only `whisper-1` (which is
            powered by our open source Whisper V2 model) is currently available.
             Example: whisper-1.
        prompt (Union[Unset, str]): An optional text to guide the model's style or continue a previous audio segment.
            The [prompt](/docs/guides/speech-to-text/prompting) should be in English.
        response_format (Union[Unset, str]): The format of the transcript output, in one of these options: `json`,
            `text`, `srt`, `verbose_json`, or `vtt`.
             Default: 'json'.
        temperature (Union[Unset, float]): The sampling temperature, between 0 and 1. Higher values like 0.8 will make
            the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0,
            the model will use [log probability](https://en.wikipedia.org/wiki/Log_probability) to automatically increase
            the temperature until certain thresholds are hit.
             Default: 0.0.
    """

    file: File
    model: Union[CreateTranslationRequestModelType1, str]
    prompt: Union[Unset, str] = UNSET
    response_format: Union[Unset, str] = "json"
    temperature: Union[Unset, float] = 0.0

    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        model: str
        if isinstance(self.model, CreateTranslationRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        prompt = self.prompt

        response_format = self.response_format

        temperature = self.temperature

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "file": file,
                "model": model,
            }
        )
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if temperature is not UNSET:
            field_dict["temperature"] = temperature

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        model: Union[CreateTranslationRequestModelType1, str]
        if isinstance(self.model, CreateTranslationRequestModelType1):
            model = (None, str(self.model.value).encode(), "text/plain")
        else:
            model = self.model

        prompt = self.prompt if isinstance(self.prompt, Unset) else (None, str(self.prompt).encode(), "text/plain")

        response_format = (
            self.response_format
            if isinstance(self.response_format, Unset)
            else (None, str(self.response_format).encode(), "text/plain")
        )

        temperature = (
            self.temperature
            if isinstance(self.temperature, Unset)
            else (None, str(self.temperature).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "file": file,
                "model": model,
            }
        )
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if temperature is not UNSET:
            field_dict["temperature"] = temperature

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file = File(payload=BytesIO(d.pop("file")))

        def _parse_model(data: object) -> Union[CreateTranslationRequestModelType1, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateTranslationRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateTranslationRequestModelType1, str], data)

        model = _parse_model(d.pop("model"))

        prompt = d.pop("prompt", UNSET)

        response_format = d.pop("response_format", UNSET)

        temperature = d.pop("temperature", UNSET)

        create_translation_request = cls(
            file=file,
            model=model,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
        )

        return create_translation_request
