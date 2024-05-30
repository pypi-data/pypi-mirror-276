from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_image_request_model_type_1 import CreateImageRequestModelType1
from ..models.create_image_request_quality import CreateImageRequestQuality
from ..models.create_image_request_response_format import CreateImageRequestResponseFormat
from ..models.create_image_request_size import CreateImageRequestSize
from ..models.create_image_request_style import CreateImageRequestStyle
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImageRequest")


@_attrs_define
class CreateImageRequest:
    """
    Attributes:
        prompt (str): A text description of the desired image(s). The maximum length is 1000 characters for `dall-e-2`
            and 4000 characters for `dall-e-3`. Example: A cute baby sea otter.
        model (Union[CreateImageRequestModelType1, None, Unset, str]): The model to use for image generation. Default:
            'dall-e-2'. Example: dall-e-3.
        n (Union[None, Unset, int]): The number of images to generate. Must be between 1 and 10. For `dall-e-3`, only
            `n=1` is supported. Default: 1. Example: 1.
        quality (Union[Unset, CreateImageRequestQuality]): The quality of the image that will be generated. `hd` creates
            images with finer details and greater consistency across the image. This param is only supported for `dall-e-3`.
            Default: CreateImageRequestQuality.STANDARD. Example: standard.
        response_format (Union[Unset, CreateImageRequestResponseFormat]): The format in which the generated images are
            returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been
            generated. Default: CreateImageRequestResponseFormat.URL. Example: url.
        size (Union[Unset, CreateImageRequestSize]): The size of the generated images. Must be one of `256x256`,
            `512x512`, or `1024x1024` for `dall-e-2`. Must be one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3`
            models. Default: CreateImageRequestSize.VALUE_2. Example: 1024x1024.
        style (Union[Unset, CreateImageRequestStyle]): The style of the generated images. Must be one of `vivid` or
            `natural`. Vivid causes the model to lean towards generating hyper-real and dramatic images. Natural causes the
            model to produce more natural, less hyper-real looking images. This param is only supported for `dall-e-3`.
            Default: CreateImageRequestStyle.VIVID. Example: vivid.
        user (Union[Unset, str]): A unique identifier representing your end-user, which can help OpenAI to monitor and
            detect abuse. [Learn more](/docs/guides/safety-best-practices/end-user-ids).
             Example: user-1234.
    """

    prompt: str
    model: Union[CreateImageRequestModelType1, None, Unset, str] = "dall-e-2"
    n: Union[None, Unset, int] = 1
    quality: Union[Unset, CreateImageRequestQuality] = CreateImageRequestQuality.STANDARD
    response_format: Union[Unset, CreateImageRequestResponseFormat] = CreateImageRequestResponseFormat.URL
    size: Union[Unset, CreateImageRequestSize] = CreateImageRequestSize.VALUE_2
    style: Union[Unset, CreateImageRequestStyle] = CreateImageRequestStyle.VIVID
    user: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt = self.prompt

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        elif isinstance(self.model, CreateImageRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        n: Union[None, Unset, int]
        if isinstance(self.n, Unset):
            n = UNSET
        else:
            n = self.n

        quality: Union[Unset, str] = UNSET
        if not isinstance(self.quality, Unset):
            quality = self.quality.value

        response_format: Union[Unset, str] = UNSET
        if not isinstance(self.response_format, Unset):
            response_format = self.response_format.value

        size: Union[Unset, str] = UNSET
        if not isinstance(self.size, Unset):
            size = self.size.value

        style: Union[Unset, str] = UNSET
        if not isinstance(self.style, Unset):
            style = self.style.value

        user = self.user

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model
        if n is not UNSET:
            field_dict["n"] = n
        if quality is not UNSET:
            field_dict["quality"] = quality
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if size is not UNSET:
            field_dict["size"] = size
        if style is not UNSET:
            field_dict["style"] = style
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        def _parse_model(data: object) -> Union[CreateImageRequestModelType1, None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateImageRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateImageRequestModelType1, None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_n(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        n = _parse_n(d.pop("n", UNSET))

        _quality = d.pop("quality", UNSET)
        quality: Union[Unset, CreateImageRequestQuality]
        if isinstance(_quality, Unset):
            quality = UNSET
        else:
            quality = CreateImageRequestQuality(_quality)

        _response_format = d.pop("response_format", UNSET)
        response_format: Union[Unset, CreateImageRequestResponseFormat]
        if isinstance(_response_format, Unset):
            response_format = UNSET
        else:
            response_format = CreateImageRequestResponseFormat(_response_format)

        _size = d.pop("size", UNSET)
        size: Union[Unset, CreateImageRequestSize]
        if isinstance(_size, Unset):
            size = UNSET
        else:
            size = CreateImageRequestSize(_size)

        _style = d.pop("style", UNSET)
        style: Union[Unset, CreateImageRequestStyle]
        if isinstance(_style, Unset):
            style = UNSET
        else:
            style = CreateImageRequestStyle(_style)

        user = d.pop("user", UNSET)

        create_image_request = cls(
            prompt=prompt,
            model=model,
            n=n,
            quality=quality,
            response_format=response_format,
            size=size,
            style=style,
            user=user,
        )

        create_image_request.additional_properties = d
        return create_image_request

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
