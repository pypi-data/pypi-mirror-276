from io import BytesIO
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_image_edit_request_model_type_1 import CreateImageEditRequestModelType1
from ..models.create_image_edit_request_response_format import CreateImageEditRequestResponseFormat
from ..models.create_image_edit_request_size import CreateImageEditRequestSize
from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="CreateImageEditRequest")


@_attrs_define
class CreateImageEditRequest:
    """
    Attributes:
        image (File): The image to edit. Must be a valid PNG file, less than 4MB, and square. If mask is not provided,
            image must have transparency, which will be used as the mask.
        prompt (str): A text description of the desired image(s). The maximum length is 1000 characters. Example: A cute
            baby sea otter wearing a beret.
        mask (Union[Unset, File]): An additional image whose fully transparent areas (e.g. where alpha is zero) indicate
            where `image` should be edited. Must be a valid PNG file, less than 4MB, and have the same dimensions as
            `image`.
        model (Union[CreateImageEditRequestModelType1, None, Unset, str]): The model to use for image generation. Only
            `dall-e-2` is supported at this time. Default: 'dall-e-2'. Example: dall-e-2.
        n (Union[None, Unset, int]): The number of images to generate. Must be between 1 and 10. Default: 1. Example: 1.
        size (Union[Unset, CreateImageEditRequestSize]): The size of the generated images. Must be one of `256x256`,
            `512x512`, or `1024x1024`. Default: CreateImageEditRequestSize.VALUE_2. Example: 1024x1024.
        response_format (Union[Unset, CreateImageEditRequestResponseFormat]): The format in which the generated images
            are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been
            generated. Default: CreateImageEditRequestResponseFormat.URL. Example: url.
        user (Union[Unset, str]): A unique identifier representing your end-user, which can help OpenAI to monitor and
            detect abuse. [Learn more](/docs/guides/safety-best-practices/end-user-ids).
             Example: user-1234.
    """

    image: File
    prompt: str
    mask: Union[Unset, File] = UNSET
    model: Union[CreateImageEditRequestModelType1, None, Unset, str] = "dall-e-2"
    n: Union[None, Unset, int] = 1
    size: Union[Unset, CreateImageEditRequestSize] = CreateImageEditRequestSize.VALUE_2
    response_format: Union[Unset, CreateImageEditRequestResponseFormat] = CreateImageEditRequestResponseFormat.URL
    user: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        image = self.image.to_tuple()

        prompt = self.prompt

        mask: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.mask, Unset):
            mask = self.mask.to_tuple()

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        elif isinstance(self.model, CreateImageEditRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        n: Union[None, Unset, int]
        if isinstance(self.n, Unset):
            n = UNSET
        else:
            n = self.n

        size: Union[Unset, str] = UNSET
        if not isinstance(self.size, Unset):
            size = self.size.value

        response_format: Union[Unset, str] = UNSET
        if not isinstance(self.response_format, Unset):
            response_format = self.response_format.value

        user = self.user

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "prompt": prompt,
            }
        )
        if mask is not UNSET:
            field_dict["mask"] = mask
        if model is not UNSET:
            field_dict["model"] = model
        if n is not UNSET:
            field_dict["n"] = n
        if size is not UNSET:
            field_dict["size"] = size
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        image = self.image.to_tuple()

        prompt = self.prompt if isinstance(self.prompt, Unset) else (None, str(self.prompt).encode(), "text/plain")

        mask: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.mask, Unset):
            mask = self.mask.to_tuple()

        model: Union[CreateImageEditRequestModelType1, None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        elif isinstance(self.model, CreateImageEditRequestModelType1):
            model = (None, str(self.model.value).encode(), "text/plain")
        else:
            model = self.model

        n: Union[None, Unset, int]
        if isinstance(self.n, Unset):
            n = UNSET
        else:
            n = self.n

        size: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.size, Unset):
            size = (None, str(self.size.value).encode(), "text/plain")

        response_format: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.response_format, Unset):
            response_format = (None, str(self.response_format.value).encode(), "text/plain")

        user = self.user if isinstance(self.user, Unset) else (None, str(self.user).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "image": image,
                "prompt": prompt,
            }
        )
        if mask is not UNSET:
            field_dict["mask"] = mask
        if model is not UNSET:
            field_dict["model"] = model
        if n is not UNSET:
            field_dict["n"] = n
        if size is not UNSET:
            field_dict["size"] = size
        if response_format is not UNSET:
            field_dict["response_format"] = response_format
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        image = File(payload=BytesIO(d.pop("image")))

        prompt = d.pop("prompt")

        _mask = d.pop("mask", UNSET)
        mask: Union[Unset, File]
        if isinstance(_mask, Unset):
            mask = UNSET
        else:
            mask = File(payload=BytesIO(_mask))

        def _parse_model(data: object) -> Union[CreateImageEditRequestModelType1, None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateImageEditRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateImageEditRequestModelType1, None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_n(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        n = _parse_n(d.pop("n", UNSET))

        _size = d.pop("size", UNSET)
        size: Union[Unset, CreateImageEditRequestSize]
        if isinstance(_size, Unset):
            size = UNSET
        else:
            size = CreateImageEditRequestSize(_size)

        _response_format = d.pop("response_format", UNSET)
        response_format: Union[Unset, CreateImageEditRequestResponseFormat]
        if isinstance(_response_format, Unset):
            response_format = UNSET
        else:
            response_format = CreateImageEditRequestResponseFormat(_response_format)

        user = d.pop("user", UNSET)

        create_image_edit_request = cls(
            image=image,
            prompt=prompt,
            mask=mask,
            model=model,
            n=n,
            size=size,
            response_format=response_format,
            user=user,
        )

        create_image_edit_request.additional_properties = d
        return create_image_edit_request

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
