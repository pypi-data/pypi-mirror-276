from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.create_speech_request_model_type_1 import CreateSpeechRequestModelType1
from ..models.create_speech_request_response_format import CreateSpeechRequestResponseFormat
from ..models.create_speech_request_voice import CreateSpeechRequestVoice
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateSpeechRequest")


@_attrs_define
class CreateSpeechRequest:
    """
    Attributes:
        model (Union[CreateSpeechRequestModelType1, str]): One of the available [TTS models](/docs/models/tts): `tts-1`
            or `tts-1-hd`
        input_ (str): The text to generate audio for. The maximum length is 4096 characters.
        voice (CreateSpeechRequestVoice): The voice to use when generating the audio. Supported voices are `alloy`,
            `echo`, `fable`, `onyx`, `nova`, and `shimmer`. Previews of the voices are available in the [Text to speech
            guide](/docs/guides/text-to-speech/voice-options).
        response_format (Union[Unset, CreateSpeechRequestResponseFormat]): The format to audio in. Supported formats are
            `mp3`, `opus`, `aac`, `flac`, `wav`, and `pcm`. Default: CreateSpeechRequestResponseFormat.MP3.
        speed (Union[Unset, float]): The speed of the generated audio. Select a value from `0.25` to `4.0`. `1.0` is the
            default. Default: 1.0.
    """

    model: Union[CreateSpeechRequestModelType1, str]
    input_: str
    voice: CreateSpeechRequestVoice
    response_format: Union[Unset, CreateSpeechRequestResponseFormat] = CreateSpeechRequestResponseFormat.MP3
    speed: Union[Unset, float] = 1.0

    def to_dict(self) -> Dict[str, Any]:
        model: str
        if isinstance(self.model, CreateSpeechRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        input_ = self.input_

        voice = self.voice.value

        response_format: Union[Unset, str] = UNSET
        if not isinstance(self.response_format, Unset):
            response_format = self.response_format.value

        speed = self.speed

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "model": model,
                "input": input_,
                "voice": voice,
            }
        )
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if speed is not UNSET:
            field_dict["speed"] = speed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_model(data: object) -> Union[CreateSpeechRequestModelType1, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateSpeechRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateSpeechRequestModelType1, str], data)

        model = _parse_model(d.pop("model"))

        input_ = d.pop("input")

        voice = CreateSpeechRequestVoice(d.pop("voice"))

        _response_format = d.pop("response_format", UNSET)
        response_format: Union[Unset, CreateSpeechRequestResponseFormat]
        if isinstance(_response_format, Unset):
            response_format = UNSET
        else:
            response_format = CreateSpeechRequestResponseFormat(_response_format)

        speed = d.pop("speed", UNSET)

        create_speech_request = cls(
            model=model,
            input_=input_,
            voice=voice,
            response_format=response_format,
            speed=speed,
        )

        return create_speech_request
